<template>
    <div class="row justify-content-center m-3 text-color-light">
      <div class="card bg-light" style="width: 24rem;">
        <div class="card-body">
          <h5 class="card-title">Manage Flagged User</h5>
          <p class="card-text">
            <strong>User Name:</strong> {{ user.name }}
          </p>
          <p class="card-text">
            You can either remove the flag from this user or delete the user from the system.
          </p>
          <div class="d-flex justify-content-between">
            <button class="btn btn-outline-success" @click="removeFlag">Remove Flag</button>
            <button class="btn btn-outline-danger" @click="deleteUser">Delete User</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        user: {
          name: "Loading...", // Placeholder while fetching
        },
      };
    },
    methods: {
      // Fetch user details
      async fetchUser() {
        try {
          const response = await fetch(
            "http://127.0.0.1:5000/get/user/" + this.$route.params.id,
            {
              method: "GET",
              mode: "cors",
              credentials: "include",
              headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + localStorage.getItem("jwt"),
              },
            }
          );
          if (response.status === 200) {
            const data = await response.json();
            this.user = data; // Populate user details
          } else if (response.status === 404) {
            alert("User not found!");
          }
        } catch (error) {
          console.error(error);
        }
      },
  
      // Remove the flag from the user
      async removeFlag() {
        if (confirm("Are you sure you want to remove the flag for this user?")) {
          try {
            const response = await fetch(
              "http://127.0.0.1:5000/unflag/user/" + this.$route.params.id,
              {
                method: "PUT",
                mode: "cors",
                credentials: "include",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: "Bearer " + localStorage.getItem("jwt"),
                },
              }
            );
            if (response.status === 200) {
              const data = await response.json();
              alert(data.message);
              this.$store.commit("unflagUser", data.resource);
              this.closeCard();
            } else {
              const data = await response.json();
              alert(data.message);
            }
          } catch (error) {
            console.error(error);
          }
        }
      },
  
      // Delete the user
      async deleteUser() {
        if (
          confirm(
            "Are you sure you want to delete this user? This action is irreversible."
          )
        ) {
          try {
            const response = await fetch(
              "http://127.0.0.1:5000/delete/user/" + this.$route.params.id,
              {
                method: "DELETE",
                mode: "cors",
                credentials: "include",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: "Bearer " + localStorage.getItem("jwt"),
                },
              }
            );
            if (response.status === 200) {
              const data = await response.json();
              alert(data.message);
              this.$store.commit("deleteUser", data.resource.id);
              this.closeCard();
            } else {
              const data = await response.json();
              alert(data.message);
            }
          } catch (error) {
            console.error(error);
          }
        }
      },
    },
    mounted() {
      this.fetchUser();
    },
  };
  </script>
  