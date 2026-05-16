<template>
    <div class="row justify-content-center m-3 text-color-light">
      <div class="card bg-light" style="width: 18rem;">
        <div class="card-body">
          <div class="d-flex justify-content-end">
            <button type="button" class="btn-close" aria-label="Close" @click="closeCard"></button>
          </div>
          <h5 class="card-title">What do you want to do?</h5>
          <div class="d-flex">
            <!-- Remove Flag Action -->
            <a class="btn btn-outline-danger me-3" @click="removeFlag">Remove Flag</a>
            <!-- Delete User Action -->
            <a class="btn btn-outline-danger" @click="deleteUser">Delete User</a>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      closeCard() {
          if (this.$route.path !== '/admin') {
            this.$router.push('/admin');
          }
      },
      // Remove flag action
      async removeFlag() {
        if (confirm("Are you sure you want to remove the flag from this sponsor?")) {
          try {
            const response = await fetch('http://127.0.0.1:5000/remove/flag/'+this.$route.params.id, {
              method: 'PUT',
              mode: 'cors',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer'+ localStorage.getItem('jwt')
              }
            });
            if (response.status === 200) {
              const data = await response.json();
              console.log(data, "Flag removed from influencer");
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
      // Delete user action
      async deleteUser() {
        if (confirm("Are you sure you want to delete this sponsor?")) {
          try {
            const response = await fetch(`http://127.0.0.1:5000/delete/user/${this.$route.params.id}`, {
              method: 'DELETE',
              mode: 'cors',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('jwt')}`
              }
            });
            if (response.status === 201) {
              const data = await response.json();
              console.log(data, "Influencer deleted");
              this.closeCard();
            } else {
              const data = await response.json();
              alert(data.message);
            }
          } catch (error) {
            console.error(error);
          }
        }
      }
    }
  };
  </script>
   -->