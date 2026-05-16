<template>
    <div>
      <nav class="navbar navbar-expand-lg navbar-dark bg-success">
          <div class="container">
              <a class="navbar-brand" href="#">sponsor dashboard</a>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                  aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarNav">
                  <ul class="navbar-nav ms-auto">
                      <li class="nav-item">
                          <a class="nav-link pointer-on-hover" @click="addcamp">addcamp</a>
                      </li>
                      <li class="nav-item">
                          <a class="nav-link pointer-on-hover" @click="notifi">noti</a>
                      </li>

                      <li class="nav-item">
                          <a class="nav-link pointer-on-hover" @click="stats" >Stats</a>
                      </li>
                      <li class="nav-item">
                          <a class="nav-link pointer-on-hover" @click="logout">logout</a>
                      </li>
                  </ul>


                      <!-- <a @click="notifi" class="nav-link pointer-on-hover ms-auto position-relative">
                        <i class="fas fa-bell" style="font-size: 1.5rem; color: white;"></i> -->
                        <!-- Badge for cart items -->
                        <!-- <span v-show="this.$store.state.notifications.length > 0"
                            class="badge bg-danger position-absolute top-0 start-100 translate-middle"
                            v-if="cartItemsCount > 0">
                            {{ this.$store.state.notifications.length }}
                        </span>
                    </a> -->

                  </div>
              </div>
          </nav>
        <main>

            

            <!-- crate a method named searchByCamp(campaigns.name,campaigns.id) -->
            <div>
                
                    <!-- Display influencer information -->
                    <h3>{{ influencerName }}</h3>
                    <p>industry: {{ influencerPlatform }}</p>
                </div>

            <ul class="list-group">




                    <li class="list-group-item" v-for="campaigns in this.$store.state.campaigns" :key="campaigns.id">
                        
                        <input @click="searchByCamp(campaigns.title, campaigns.id)"
                            class="form-check-input me-1 pointer-on-hover" type="radio" :name="campaigns.name"
                            :value="campaigns.id" :id="campaigns.id" :checked="checkedValue === campaigns.id">
                        <label class="form-check-label" :for="campaigns.id">{{ campaigns.title }}</label>
                        <p>{{campaigns}}</p>
                        <label class="form-check-label" :for="campaigns.id">{{ campaigns.description }}</label>
                        <label class="form-check-label" :for="campaigns.id">{{ campaigns.enddate }}</label>
                        <label class="form-check-label" :for="campaigns.id">{{ campaigns.budget }}</label>



                        <!-- how to edit the campaigns -->
                        <!-- also need to create a method named editcamp,delcamp and viewcamp -->
                        <a class="pointer-on-hover" @click="editcamp(campaigns.id)">edit</a>
                    </li>




                    <strong>requests from influencer</strong>

                    <li class="list-group-item" v-for="notification in this.$store.state.notifications" :key="notification.id">
                        <!-- Notification Title and Details -->
                        <div>
                            <strong>{{ notification.title }}</strong><br>
                            <label class="form-check-label">{{ notification.description }}</label><br>
                            <label class="form-check-label">{{ notification.influencer }}</label><br>
                        </div>

                        <!-- Accept and Reject Options -->
                        <div class="d-flex justify-content-end">
                            <button class="btn btn-outline-success btn-sm me-2" @click="acceptnoti(notification.id)">
                                action
                            </button>
                            <button class="btn btn-outline-success btn-sm me-2" @click="rejectnoti(notification.id)">
                                reject
                            </button>
                        </div>
                    </li>




                    <strong>completed campaigns nned to verify</strong>

                    <li class="list-group-item" v-for="notification in this.$store.state.notifications1" :key="notification.id">
                        <!-- Notification Title and Details -->
                        <div>
                            <strong>{{ notification.title }}</strong><br>
                            <label class="form-check-label">{{ notification.description }}</label><br>
                            <label class="form-check-label">{{ notification.influencer }}</label><br>
                        </div>

                        <!-- Accept and Reject Options -->
                        <div class="d-flex justify-content-end">
                            <button class="btn btn-outline-success btn-sm me-2" @click="acceptnotif(notification.id)">
                                action
                            </button>
                            <button class="btn btn-outline-success btn-sm me-2" @click="rejectnotif(notification.id)">
                                reject
                            </button>
                        </div>
                    </li>










                    <strong>completed campaigns</strong>

                    <li class="list-group-item" v-for="notification in this.$store.state.notifications2" :key="notification.id">
                        <!-- Notification Title and Details -->
                        <div>
                            <strong>{{ notification.title }}</strong><br>
                            <label class="form-check-label">{{ notification.budget }}</label><br>
                            <label class="form-check-label">{{ notification.influencer }}</label><br>
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
        influencerPlatform: '' // Store influencer platform
    };
  }, 
  methods: {


    notifi() {
            if (this.$route.path != '/spon/notifications') {
                this.$router.push('/spon/notifications')
            }
        },


    handleFileUpload(event) {
        this.profilePic = event.target.files[0];
    },



    editcamp(id) {
            if (this.$route.path != '/spon/camp/edit/' + id) {
                this.$router.push('/spon/camp/edit/' + id)
            }
    },
    findinflu(id) {
            if (this.$route.path != '/spon/find/influ/' + id) {
                this.$router.push('/spon/find/influ/' + id)
            }
    },





    async searchByCampaign(campaignName, campaignId) {
    this.checkedValue = campaignId;
    try {
        const response = await fetch('http://127.0.0.1:5000/search/by/campaign', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
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




async rejectnoti(notificationId) {
  if (confirm("Are you sure you want to reject this influencer?")) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/delete/notification/${notificationId}`, {
        method: 'DELETE',
        mode: 'cors',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('jwt')
        },
        body: JSON.stringify({ id: notificationId })  // Sending the notification ID
      });

      if (response.status === 200) {
        const data = await response.json();
        // Assuming the response contains the notification ID to be removed
        this.$store.commit('removeNotification', notificationId);
        console.log("Notification rejected and removed from store.");
      } else {
        const data = await response.json();
        alert(data.message);  // Alert if something went wrong
      }
    } catch (error) {
      console.error("Error rejecting notification:", error);
    }
  }
},








async rejectnotif(notificationId) {
  if (confirm("Are you sure you want to reject this influencer?")) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/delete/notification1/${notificationId}`, {
        method: 'DELETE',
        mode: 'cors',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('jwt')
        },
        body: JSON.stringify({ id: notificationId })  // Sending the notification ID
      });

      if (response.status === 200) {
        const data = await response.json();
        // Assuming the response contains the notification ID to be removed
        this.$store.commit('deleteNotification1', notificationId);
        console.log("Notification rejected and removed from store.");
      } else {
        const data = await response.json();
        alert(data.message);  // Alert if something went wrong
      }
    } catch (error) {
      console.error("Error rejecting notification:", error);
    }
  }
},










async acceptnoti(campaignId) {
  if (confirm("Are you sure you want to accept this campaign?")) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/accept/influencer/${campaignId}`, {
        method: 'PUT',  // Use PUT for accepting the campaign
        mode: 'cors',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('jwt')
        },
        body: JSON.stringify({ id: campaignId })  // Sending the campaign ID
      });

      if (response.status === 200) {
        const data = await response.json();
        // Assuming the response contains the campaign ID to be accepted
        this.$store.commit('setAccepCamps', data);
        this.$store.commit('removeNotification', notificationId);  // Update the store to reflect the accepted campaign
        console.log("inflluencer accepted and updated in store.");
      } else {
        const data = await response.json();
        alert(data.message);  // Alert if something went wrong
      }
    } catch (error) {
      console.error("Error accepting campaign:", error);
    }
  }
},




async acceptnotif(campaignId) {
  if (confirm("Are you sure you want to accept this campaign?")) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/accept/influencerproof/${campaignId}`, {
        method: 'PUT',  // Use PUT for accepting the campaign
        mode: 'cors',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('jwt')
        },
        body: JSON.stringify({ id: campaignId })  // Sending the campaign ID
      });

      if (response.status === 200) {
        const data = await response.json();
        // Assuming the response contains the campaign ID to be accepted
        this.$store.commit('setNotifications1', data);
        console.log("inflluencer accepted and updated in store.");
      } else {
        const data = await response.json();
        alert(data.message);  // Alert if something went wrong
      }
    } catch (error) {
      console.error("Error accepting campaign:", error);
    }
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
                    this.$store.commit('setCampaigns', data.campaign)
                } else {
                    const data = await response.json();
                    alert(data.message);
                }
            } catch (error) {
                console.error(error);
            }
        },




    // all the important links


    
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
    addcamp(){
        if (this.$route.path != '/spon/camp/add') {
            this.$router.push('/spon/camp/add')
        }
    },


       


    
  },
  mounted(){
    const source = new EventSource("/stream");
    this.influencerName = localStorage.getItem('email');
    this.influencerPlatform = localStorage.getItem('industry');
    source.addEventListener('notifyspon', event => {
          let data = JSON.parse(event.data);
          alert(data.message)
        }, false);
    this.$store.dispatch('fetchCampaigns')
    this.$store.dispatch('fetchNotifications')
    this.$store.dispatch('fetchNotifications1')
    this.$store.dispatch('fetchNotifications2')

  } 
  }
  </script> -->