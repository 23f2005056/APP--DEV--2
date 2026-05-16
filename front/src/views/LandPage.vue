<template>
  <div class="container text-center mt-5">
    <h1 class="mb-4">Welcome to Influencer Engagement & Sponsorship Coordination Platform</h1>
    <p class="mb-4">Please login to continue</p>
    <div class="d-flex justify-content-center">
      <a class="btn btn-outline-dark btn-sm" @click="login">Login</a>
      <a class="btn btn-outline-dark btn-sm" @click="register">Register</a>
    </div>
  </div>

  <!-- <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script> -->
</template>



<script>
export default {
  methods: {
    login() {
      if (this.$route.path != '/login') {
        this.$router.push('/login')
      }
    },
    register() {
      if (this.$route.path != '/register') {
        this.$router.push('/register')
      }
    },
    async fetchUser() {
      try {
        const response = await fetch('http://127.0.0.1:5000/auth/user', {
          method: 'GET',
          mode: 'cors',
          credentials: 'include',
          headers: {
            'access_token': localStorage.getItem('access_token'),
            'Content-Type': 'application/json',
          },
        });
      } catch (error) {
        console.error(error);
      }
    },
  },
  mounted() {
    this.fetchUser()
  }
}
</script>