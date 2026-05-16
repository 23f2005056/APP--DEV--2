<template>
    <div>
      <nav class="navbar navbar-expand-lg navbar-dark bg-success">
          <div class="container">
              <a class="navbar-brand" href="#">admin dashboard</a>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                  aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarNav">
                  <ul class="navbar-nav ms-auto">
                      <li class="nav-item">
                          <a class="nav-link pointer-on-hover" @click="campaigns">campaigns</a>
                      </li>
                      <li class="nav-item">
                          <a class="nav-link pointer-on-hover" @click="user">users</a>
                      </li>
                      <li class="nav-item">
                          <a class="nav-link pointer-on-hover" @click="stats" >Stats</a>
                      </li>
                      <li class="nav-item">
                          <a class="nav-link pointer-on-hover" @click="logout">logout</a>
                      </li>
                  </ul>
  
                      <!-- Search Bar  -->
                      <form class="d-flex ms-auto" @submit.prevent="search">
                          <input class="form-control me-2" type="search" v-model="query" placeholder="Search"
                              aria-label="Search">
                          <button class="btn btn-outline-light" type="submit">Search</button>
                      </form>  


                      <a @click="notifi" class="nav-link pointer-on-hover ms-auto position-relative">
                        <i class="fas fa-bell" style="font-size: 1.5rem; color: white;"></i>
                        <!-- Badge for cart items -->
                        <span v-show="this.$store.state.notifications.length > 0"
                            class="badge bg-danger position-absolute top-0 start-100 translate-middle"
                            v-if="cartItemsCount > 0">
                            {{ this.$store.state.notifications.length }}
                        </span>
                    </a>

                  </div>
              </div>
          </nav>
        <main>


            <ul class="list-group">
              <li v-for="campaign in this.$store.state.flaginfluencer" :key="campaign.id" class="list-group-item">
                <div class="d-flex justify-content-between">

                  <div>
                  <strong>{{ campaign.email }}</strong><br>
                  </div>

                  <div>
                  <button class="btn btn-outline-primary btn-sm pointer-on-hover" @click="actioninfl(campaign.id)">
                  action
                  </button>
                  </div>

                </div>
              </li>

              <li v-for="campaign in this.$store.state.flagsponsor" :key="campaign.id" class="list-group-item">
                <div class="d-flex justify-content-between">

                  <div>
                  <strong>{{ campaign.email }}</strong><br>
                  </div>

                  <div>
                  <button class="btn btn-outline-primary btn-sm pointer-on-hover" @click="actionspon(campaign.id)">action</button>
                  </div>

                </div>
              </li>
            </ul>


            <router-view></router-view>
        </main>
    </div>
  </template>
  
   <script>
  export default {
    data() {
    return {
        cartItemsCount: 1,
        checkedValue: -1
    };
  }, 
  methods: {

    actioninfl(id) {
            if (this.$route.path != '/admin/influ/' + id) {
                this.$router.push('/admin/influ/' + id)
            }
    },
    actionspon(id) {
            if (this.$route.path != '/admin/spon/' + id) {
                this.$router.push('/admin/spon/' + id)
            }
    },


    

async search() {
            try {
                const response = await fetch('http://127.0.0.1:5000/search/for', {
                    method: 'POST',
                    headers: {

                        'Content-type': 'application/json'
                    },
                    body: JSON.stringify({
                        "query": this.query
                    }),
                });
                if (response.status === 200) {
                    const data = await response.json();
                    console.log(data.cat, "searched for campaign")
                    this.$store.commit('setcampaigns', data.campaign)
                } else {
                    const data = await response.json();
                    alert(data.message);
                }
            } catch (error) {
                console.error(error);
            }
        },


    


    // all the important links

    campaigns(){
        if (this.$route.path != '/admin/camp') {  
             this.$router.push('/admin/camp') // # meaning influencer other campaigns
        }
    },
    user(){
        if (this.$route.path != '/admin/user') {  
             this.$router.push('/admin/user') // # meaning influencer other campaigns
        }
    },
    async logout() {
            localStorage.removeItem('jwt');
            localStorage.removeItem('role');
            if (this.$route.path != '/') {
                this.$router.push('/')
            }
    },
    stats(){
        if (this.$route.path != '/report') {
            this.$router.push('/report')
        }
    },

    
  },
mounted(){
    const source = new EventSource("/stream");
    source.addEventListener('notifyadmin', event => {
          let data = JSON.parse(event.data);
          alert(data.message)
        }, false);
    this.$store.dispatch('fetchFlagInfluencers')
    this.$store.dispatch('fetchFlagSponsor')
  } 
}
  </script> -->