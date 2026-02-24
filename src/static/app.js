document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message and reset activity select options
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        `;

        // Append participants section (compact, no bullets) with delete buttons
        if (details.participants && details.participants.length) {
          const participantsHeading = document.createElement("p");
          participantsHeading.innerHTML = "<strong>Participants:</strong>";
          participantsHeading.style.marginTop = "8px";
          activityCard.appendChild(participantsHeading);

          const ul = document.createElement("ul");
          ul.className = "participants";
          details.participants.forEach((p) => {
            const li = document.createElement("li");
            li.className = "participant-item";

            const span = document.createElement("span");
            span.className = "participant-email";
            span.textContent = p;

            const delBtn = document.createElement("button");
            delBtn.type = "button";
            delBtn.className = "delete-participant";
            delBtn.title = "Remove participant";
            delBtn.innerHTML = "✖";

            // Delete handler: call backend to remove participant and refresh list
            delBtn.addEventListener("click", async () => {
              if (!confirm(`Remove ${p} from ${name}?`)) return;
              try {
                const resp = await fetch(
                  `/activities/${encodeURIComponent(name)}/participants?email=${encodeURIComponent(p)}`,
                  { method: "DELETE" }
                );
                const resJson = await resp.json();
                if (resp.ok) {
                  messageDiv.textContent = resJson.message;
                  messageDiv.className = "success";
                  messageDiv.classList.remove("hidden");
                  // Refresh activities to reflect change
                  fetchActivities();
                } else {
                  messageDiv.textContent = resJson.detail || "Failed to remove participant";
                  messageDiv.className = "error";
                  messageDiv.classList.remove("hidden");
                }
                setTimeout(() => {
                  messageDiv.classList.add("hidden");
                }, 4000);
              } catch (error) {
                console.error("Error removing participant:", error);
                messageDiv.textContent = "Failed to remove participant.";
                messageDiv.className = "error";
                messageDiv.classList.remove("hidden");
                setTimeout(() => {
                  messageDiv.classList.add("hidden");
                }, 4000);
              }
            });

            li.appendChild(span);
            li.appendChild(delBtn);
            ul.appendChild(li);
          });
          activityCard.appendChild(ul);
        } else {
          const noParticipants = document.createElement("p");
          noParticipants.className = "info";
          noParticipants.textContent = "No participants yet.";
          noParticipants.style.marginTop = "8px";
          activityCard.appendChild(noParticipants);
        }

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "message success";
        signupForm.reset();

        // Refresh activities so UI reflects new participant immediately
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "message error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
      } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "message error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
