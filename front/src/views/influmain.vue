<template>
    <div>
      <nav class="navbar navbar-expand-lg navbar-dark bg-success">
          <div class="container">
              <a class="navbar-brand" href="#">influencer dashboard</a>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                  aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarNav">
                  <ul class="navbar-nav ms-auto">
                      <li class="nav-item">
                          <a class="nav-link pointer-on-hover" @click="camps">camps</a>
                      </li>
                      <li class="nav-item">
                          <a class="nav-link pointer-on-hover" @click="stats" >Stats</a>
                      </li>
                      <li class="nav-item">
                          <a class="nav-link pointer-on-hover" @click="logout">logout</a>
                      </li>
                  </ul>
  
                      <!-- Search Bar -->
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

            

            <!-- crate a method named searchByCamp(campaigns.name,campaigns.id) -->


            <ul class="list-group">
                <div>
                    <!-- Display influencer information -->
                    <h3>{{ influencerName }}</h3>
                    <p>Platform: {{ influencerPlatform }}</p>
                    <p>followers: {{ influencerfollowers }}</p>
                </div>

            
                    <h1>my campaigns</h1>
                    <li class="list-group-item" v-for="campaigns in this.$store.state.campaigns" :key="campaigns.id">
                        
                        
                        <!-- need to create an async method named search by camp in this page only line 114. see reference code n git line 114 -->
                        <!-- i neeed to creaate that method in models bealow -->
                        
                    <div class="form-check mb-2">
                    <input 
                        @click="searchByCamp(campaigns.name, campaigns.id)" 
                        class="form-check-input me-1 pointer-on-hover" 
                        type="radio" 
                        :name="campaigns.name" 
                        :value="campaigns.id" 
                        :id="campaigns.id" 
                        :checked="checkedValue === campaigns.id"
                    >
                    <label class="form-check-label" :for="campaigns.id">
                        <span>Title: {{ campaigns.title }}</span><br>
                        <span>Budget: {{ campaigns.budget }}</span><br>
                        <span>End Date: {{ campaigns.enddate }}</span><br>
                        <span>Description: {{ campaigns.description }}</span>
                        
                    </label>
                    </div>



                        <!-- how to edit the campaigns -->
                        <!-- also need to create a method named editcamp,delcamp and viewcamp -->
                        <a class="pointer-on-hover" @click="compcamp(campaigns.id)">campaig cmpletion</a>

                    </li>









                    <strong>completed campaigns</strong>
                    <li class="list-group-item" v-for="notification in this.$store.state.notifications3" :key="notification.id">
                        <!-- Notification Title and Details -->
                        <div>
                            <strong>{{ notification.title }}</strong><br>
                            <label class="form-check-label">{{ notification.budget }}</label><br>
                            <label class="form-check-label">{{ notification.influencer }}</label><br>
                        </div>
                    </li>




                    <strong>searched campaigns</strong>
                    <li class="list-group-item" v-for="notification in this.$store.state.notifications2" :key="notification.id">
                        <!-- Notification Title and Details -->
                        <div>
                            <strong>{{ notification.title }}</strong><br>
                            <label class="form-check-label">{{ notification.budget }}</label><br>
                            <label class="form-check-label">{{ notification.end_date }}</label><br>
                            <label class="form-check-label">{{ notification.description }}</label><br>

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
        checkedValue: -1,
        influencerName: '', // Store influencer name
        influencerPlatform: '', // Store influencer platform
        influencerfollowers: '' // Store influencer sponsors
    };
  }, 
  methods: {

    compcamp(id) {
            if (this.$route.path != '/influ/camp/comp/' + id) {
                this.$router.push('/influ/camp/comp/' + id)
            }
    },


    notifi() {
        if (this.$route.path != '/influ/noti') {
            this.$router.push('/influ/noti')
        }
    },



    async searchByCampaign(campaignName, campaignId) {
    this.checkedValue = campaignId;
    try {
        const response = await fetch('http://127.0.0.1:5000/search/by/campaign', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('jwt')
            },
            body: JSON.stringify({
                "query": campaignName
            }),
        });

        if (response.status === 200) {
            const data = await response.json();
            this.$store.commit('setCampaigns', data.campaigns);
            console.log(data.resource);
        } else {
            const data = await response.json();
            alert(data.message);
        }
    } catch (error) {
        console.error(error);
    }
},



async search() {
            try {
                const response = await fetch('http://127.0.0.1:5000/search/for', {
                    method: 'POST',
                    headers: {

                        'Content-type': 'application/json',
                        'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                    },
                    body: JSON.stringify({
                        "query": this.query
                    }),
                });
                if (response.status === 200) {
                    const data = await response.json();
                    console.log(data.campaigns, "searched for campaign")
                    this.$store.commit('setNotifications2', data.campaigns)
                } else {
                    const data = await response.json();
                    alert(data.message);
                }
            } catch (error) {
                console.error(error);
            }
        },



    // all the important links

    camps(){
        if (this.$route.path != '/influ/camp') {
            this.$router.push('/influ/camp')
        }
    },
    mycamp(){
        if (this.$route.path != '/influ/mycamp') {
            this.$router.push('/influ/mycamp')
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
    this.influencerName = localStorage.getItem('email');
    this.influencerPlatform = localStorage.getItem('platform');
    this.influencerfollowers = localStorage.getItem('followers');
    const source = new EventSource("/stream");
    source.addEventListener('notifyadmin', event => {
          let data = JSON.parse(event.data);
          alert(data.message)
        }, false);
    this.$store.dispatch('fetchCampaigns')
    this.$store.dispatch('fetchNoti')
    this.$store.dispatch('fetchNotifications3')
  } 
  }
  </script> -->
  