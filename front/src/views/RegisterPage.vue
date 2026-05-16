<template>
  <div class="row justify-content-center m-3 text-color-light">
    <div class="card bg-light" style="width: 18rem;">
      <div class="card-body">
        <h5 class="card-title">Sign up</h5>
        <form @submit.prevent="submitForm">
          <div class="mb-3">
            <label class="form-label">Email address</label>
            <input type="email" v-model="email" class="form-control">
            <div v-if="message" class="alert alert-warning">
              {{ message }}
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" v-model="password" class="form-control">
          </div>
          <div class="mb-3">
            <select class="input is-large" v-model="userType" required>
              <option class="input is-large" value="influencer">influencer</option>
              <option class="input is-large" value="sponsor">sponsor</option>
            </select>
          </div>
          <!-- Show company field for sponsors -->
          <input v-if="userType === 'sponsor'" v-model="industry" type="text" placeholder="Industry" required />
          
          <!-- Show platform, followers, and niche fields for influencers -->
          <input v-if="userType === 'influencer'" v-model="platform" type="text" placeholder="platform (e.g., Instagram)" />
          <input v-if="userType === 'influencer'" v-model="followers" type="number" placeholder="Followers Count" />
          
          <button type="submit" class="btn btn-outline-primary">Sign up</button>
        </form>
      </div>
    </div>
  </div>
</template>


<script>

export default {
  name: 'registerpage',
  data() {
    return {
      email: '',
      password: '',
      role: '',
      message: '',
      industry:''
    }
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('http://127.0.0.1:5000/signup', {
          method: 'POST',
          mode: 'cors',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({
            "email": this.email,
            "password": this.password,
            "role": this.userType,
            "platform":this.platform,
            "followers":this.followers,
            "industry":this.industry
          }),
        });
        console.log(response.status)
        if (response.status === 201) {
          console.log("data")
          // const data = await response.json();
          console.log(data)
          alert("User created successfully");
          alert(data.message);
          if (this.$route.path != '/login') {
            console.log("dd2")
            this.$router.push('/login')
            this.closeCard()
          }
        } else if (response.status === 409) {
          console.log("dd3")
          const data = await response.json();
          alert(data.msg);
        }
      } catch (error) {
        console.error(error);
        alert("Something went wrong. Please try again later.");
      }
      this.$router.push('/login')
    },
  }
}
</script>sponsor