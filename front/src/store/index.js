import { createStore } from 'vuex';
import axios from 'axios';
const store = createStore({
  state: {
    influencer:[],
    sponsor:[],
    flagsponsor:[],
    falginfluencer:[],
    notifications:[],
    notifications1:[],
    notifications2:[],
    notifications3:[],

    campaigns:[],
    proof:[],
    othercamp:[],
    industry:[],
    authenticatedUser:[],
    flaguser:[],
    accepcamp:[],
    yourcamp:[],
    complecamp:[],
    compleconfirmcap:[],
    spocamp:[]
  },
  getters: {
    getfalgsponsor: state => state.flagsponsor,
    getflaginfluencer: state => state.falginfluencer,
    getCampaigns: state => state.campaigns,
    getfalguser: state => state.flaguser,
    getnotifications: state => state.notifications,
    getnotifications2: state => state.notifications2,
    getnotifications3: state => state.notifications3,
    getnotifications1: state => state.notifications1,
    getinfluencer: state => state.influencer,
    getsponsor: state => state.sponsor,
    getothercamp: state => state.othercamp,
    getproof: state => state.proof,
    getaccepcamp: state => state.accepcamp,
    getauthenticatedUser: state => state.authenticatedUser,
    getspocamp: state => state.spocamp,
    getyourcamp: state => state.yourcamp,
    getcompleconfirmcamp: state => state.compleconfirmcamp,
    getcomplecamp: state => state.complecamp,
    getTotalAmount: state => {
      return state.complecamp.reduce((total, complecamp) => total + complecamp.budget, 0);
    },
  },
  mutations: {


    setFlagInfluencer: (state, flaggedInfluencers) => {
        state.flaginfluencer = flaggedInfluencers;
      },
      addFlagInfluencer: (state, newFlaggedInfluencer) => {
        state.flaginfluencer.push(newFlaggedInfluencer);
      },
      updateFlagInfluencer: (state, updatedFlaggedInfluencer) => {
        const index = state.flaginfluencer.findIndex(
          influencer => influencer.id === updatedFlaggedInfluencer.id
        );
        if (index !== -1) {
          state.flaginfluencer.splice(index, 1, updatedFlaggedInfluencer);
        }
      },
      deleteFlagInfluencer: (state, influencerId) => {
        state.flaginfluencer = state.flaginfluencer.filter(
          influencer => influencer.id !== influencerId
        );
      },

      




      setNotifications3: (state, notifications3) => {
        state.notifications3 = notifications3;
    },
    addNotification3: (state, newNotification3) => {
        state.notifications3.push(newNotification3);
    },
    updateNotification3: (state, updatedNotification3) => {
        const index = state.notifications3.findIndex(n => n.id === updatedNotification3.id);
        if (index !== -1) {
            state.notifications3.splice(index, 1, updatedNotification3);
        }
    },
    deleteNotification3: (state, notificationId3) => {
        state.notifications3 = state.notifications3.filter(n => n.id !== notificationId3);
    },
    



      setFlagSponsor: (state, flaggedSponsors) => {
        state.flagsponsor = flaggedSponsors;
      },
      addFlagSponsor: (state, newFlaggedSponsor) => {
        state.flagsponsor.push(newFlaggedSponsor);
      },
      updateFlagSponsor: (state, updatedFlaggedSponsor) => {
        const index = state.flagsponsor.findIndex(
          sponsor => sponsor.id === updatedFlaggedSponsor.id
        );
        if (index !== -1) {
          state.flagsponsor.splice(index, 1, updatedFlaggedSponsor);
        }
      },
      deleteFlagSponsor: (state, sponsorId) => {
        state.flagsponsor = state.flagsponsor.filter(
          sponsor => sponsor.id !== sponsorId
        );
      },

      





    setFlagUser: (state, flaggedUsers) => {
        state.flaguser = flaggedUsers;
      },
      addFlagUser: (state, newFlaggedUser) => {
        state.flaguser.push(newFlaggedUser);
      },
      updateFlagUser: (state, updatedFlaggedUser) => {
        const index = state.flaguser.findIndex(user => user.id === updatedFlaggedUser.id);
        if (index !== -1) {
          state.flaguser.splice(index, 1, updatedFlaggedUser);
        }
      },
      deleteFlagUser: (state, userId) => {
        state.flaguser = state.flaguser.filter(user => user.id !== userId);
      },
      



        setYourCamp: (state, campaigns) => {
            state.yourcamp = campaigns;
          },
          addYourCamp: (state, newCampaign) => {
            state.yourcamp.push(newCampaign);
          },
          updateYourCamp: (state, updatedCampaign) => {
            const index = state.yourcamp.findIndex(campaign => campaign.id === updatedCampaign.id);
            if (index !== -1) {
              state.yourcamp.splice(index, 1, updatedCampaign);
            }
          },
          deleteYourCamp: (state, campaignId) => {
            state.yourcamp = state.yourcamp.filter(campaign => campaign.id !== campaignId);
          },
        




        setOtherCamp: (state, campaigns) => {
            state.othercamp = campaigns;
        },
        addOtherCamp: (state, newCampaign) => {
            state.othercamp.push(newCampaign);
        },
        updateOtherCamp: (state, updatedCampaign) => {
            const index = state.othercamp.findIndex(campaign => campaign.id === updatedCampaign.id);
            if (index !== -1) {
                state.othercamp.splice(index, 1, updatedCampaign);
            }
        },
        deleteOtherCamp: (state, campaignId) => {
            state.othercamp = state.othercamp.filter(campaign => campaign.id !== campaignId);
        },
        



        setCompleConfirmCap: (state, campaigns) => {
            state.compleconfirmcap = campaigns;
          },
          addCompleConfirmCap: (state, newCampaign) => {
            state.compleconfirmcap.push(newCampaign);
          },
          updateCompleConfirmCap: (state, updatedCampaign) => {
            const index = state.compleconfirmcap.findIndex(campaign => campaign.id === updatedCampaign.id);
            if (index !== -1) {
              state.compleconfirmcap.splice(index, 1, updatedCampaign);
            }
          },
          deleteCompleConfirmCap: (state, campaignId) => {
            state.compleconfirmcap = state.compleconfirmcap.filter(campaign => campaign.id !== campaignId);
          },




      setinfluencer: (state, influencer) => {
          state.influencer = influencer;
      },
      addinfluencer: (state, newinfluencer) => {
          state.influencer.push(newinfluencer);
      },
      updateinfluencer: (state, updatedinfluencer) => {
          const index = state.influencer.findIndex(i => i.id === updatedinfluencer.id);
          if (index !== -1) {
              state.influencers.splice(index, 1, updatedinfluencer);
          }
      },
      deleteinfluencer: (state, influencerId) => {
          state.influencer = state.influencers.filter(i => i.id !== influencerId);
      },



        setSponsor: (state, sponsors) => {
            state.sponsor = sponsors;
        },
        addSponsor: (state, newSponsor) => {
            state.sponsor.push(newSponsor);
        },
        updateSponsor: (state, updatedSponsor) => {
            const index = state.sponsor.findIndex(s => s.id === updatedSponsor.id);
            if (index !== -1) {
                state.sponsor.splice(index, 1, updatedSponsor);
            }
        },
        deleteSponsor: (state, sponsorId) => {
            state.sponsor = state.sponsor.filter(s => s.id !== sponsorId);
        },



        setNotifications: (state, notifications) => {
            state.notifications = notifications;
        },
        addNotification: (state, newNotification) => {
            state.notifications.push(newNotification);
        },
        updateNotification: (state, updatedNotification) => {
            const index = state.notifications.findIndex(n => n.id === updatedNotification.id);
            if (index !== -1) {
                state.notifications.splice(index, 1, updatedNotification);
            }
        },
        deleteNotification: (state, notificationId) => {
            state.notifications = state.notifications.filter(n => n.id !== notificationId);
        },


        setNotifications1: (state, notifications1) => {
          state.notifications1 = notifications1;
        },
        addNotification1: (state, newNotification1) => {
            state.notifications1.push(newNotification1);
        },
        updateNotification1: (state, updatedNotification1) => {
            const index = state.notifications1.findIndex(n => n.id === updatedNotification1.id);
            if (index !== -1) {
                state.notifications1.splice(index, 1, updatedNotification1);
            }
        },
        deleteNotification1: (state, notificationId1) => {
            state.notifications1 = state.notifications1.filter(n => n.id !== notificationId1);
        },




        setNotifications2: (state, notifications2) => {
          state.notifications2 = notifications2;
      },
      addNotification2: (state, newNotification2) => {
          state.notifications2.push(newNotification2);
      },
      updateNotification2: (state, updatedNotification2) => {
          const index = state.notifications2.findIndex(n => n.id === updatedNotification2.id);
          if (index !== -1) {
              state.notifications2.splice(index, 1, updatedNotification2);
          }
      },
      deleteNotification2: (state, notificationId2) => {
          state.notifications1 = state.notifications2.filter(n => n.id !== notificationId2);
      },
      
        


        setCampaigns: (state, campaigns) => {
            state.campaigns = campaigns;
        },
        addCampaign: (state, newCampaign) => {
            state.campaigns.push(newCampaign);
        },
        updateCampaign: (state, updatedCampaign) => {
            const index = state.campaigns.findIndex(c => c.id === updatedCampaign.id);
            if (index !== -1) {
                state.campaigns.splice(index, 1, updatedCampaign);
            }
        },
        deleteCampaign: (state, campaignId) => {
            state.campaigns = state.campaigns.filter(c => c.id !== campaignId);
        },




        setProofs: (state, proofs) => {
            state.proofs = proofs;
        },
        addProof: (state, newProof) => {
            state.proofs.push(newProof);
        },
        updateProof: (state, updatedProof) => {
            const index = state.proofs.findIndex(p => p.id === updatedProof.id);
            if (index !== -1) {
                state.proofs.splice(index, 1, updatedProof);
            }
        },
        deleteProof: (state, proofId) => {
            state.proofs = state.proofs.filter(p => p.id !== proofId);
        },



        setIndustries: (state, industries) => {
            state.industries = industries;
        },
        addIndustry: (state, newIndustry) => {
            state.industries.push(newIndustry);
        },
        updateIndustry: (state, updatedIndustry) => {
            const index = state.industries.findIndex(i => i.id === updatedIndustry.id);
            if (index !== -1) {
                state.industries.splice(index, 1, updatedIndustry);
            }
        },
        deleteIndustry: (state, industryId) => {
            state.industries = state.industries.filter(i => i.id !== industryId);
        },



        setAuthenticatedUser: (state, authenticatedUser) => {
            state.authenticatedUser = authenticatedUser;
        },
        addAuthenticatedUser: (state, newAuthenticatedUser) => {
            state.authenticatedUser.push(newAuthenticatedUser);
        },
        updateAuthenticatedUser: (state, updatedAuthenticatedUser) => {
            const index = state.authenticatedUser.findIndex(u => u.id === updatedAuthenticatedUser.id);
            if (index !== -1) {
                state.authenticatedUser.splice(index, 1, updatedAuthenticatedUser);
            }
        },
        deleteAuthenticatedUser: (state, authenticatedUserId) => {
            state.authenticatedUser = state.authenticatedUser.filter(u => u.id !== authenticatedUserId);
        },



        setAccepCamps: (state, accepcamp) => {
            state.accepcamp = accepcamp;  // Replace the current list with a new one
        },
        // Add a new accepted campaign
        addAccepCamp: (state, newAccepCamp) => {
            state.accepcamp.push(newAccepCamp);  // Append the new campaign to the list
        },
        // Update an existing accepted campaign
        updateAccepCamp: (state, updatedAccepCamp) => {
            const index = state.accepcamp.findIndex(a => a.id === updatedAccepCamp.id);
            if (index !== -1) {
                state.accepcamp.splice(index, 1, updatedAccepCamp);  // Update the campaign at the found index
            }
        },
        // Delete an accepted campaign by ID
        deleteAccepCamp: (state, accepCampId) => {
            state.accepcamp = state.accepcamp.filter(a => a.id !== accepCampId);  // Filter out the campaign to delete
        },



        setCompleCamps: (state, compleCamps) => {
            state.compleCamps = compleCamps;
        },
        addCompleCamp: (state, newCompleCamp) => {
            state.compleCamps.push(newCompleCamp);
        },
        updateCompleCamp: (state, updatedCompleCamp) => {
            const index = state.compleCamps.findIndex(c => c.id === updatedCompleCamp.id);
            if (index !== -1) {
                state.compleCamps.splice(index, 1, updatedCompleCamp);
            }
        },
        deleteCompleCamp: (state, compleCampId) => {
            state.compleCamps = state.compleCamps.filter(c => c.id !== compleCampId);
        },



        setSpoCamps: (state, spoCamps) => {
            state.spoCamps = spoCamps;
        },
        addSpoCamp: (state, newSpoCamp) => {
            state.spoCamps.push(newSpoCamp);
        },
        updateSpoCamp: (state, updatedSpoCamp) => {
            const index = state.spoCamps.findIndex(s => s.id === updatedSpoCamp.id);
            if (index !== -1) {
                state.spoCamps.splice(index, 1, updatedSpoCamp);
            }
        },
        deleteSpoCamp: (state, spoCampId) => {
            state.spoCamps = state.spoCamps.filter(s => s.id !== spoCampId);
        },

  


    
},


    
actions: {


    async fetchUnflaggedinfluencer({ commit }) {
        try {
          const response = await fetch("http://127.0.0.1:5000/get/unflagged-influencer", {
            method: "GET",
            mode: "cors",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Bearer " + localStorage.getItem("jwt"),
            },
          });
  
          if (response.status === 200) {
            const data = await response.json();
            console.log(data, 'unflagged influencer fetched');
            commit('setinfluencer', data.resource); // Commit to Vuex store
          } else {
            alert("Failed to fetch unflaginfluencer");}
        } catch (error) {
            console.error('Error fetching flagged influencers:', error);
        }
      },



      async fetchUnflaggedsponsor({ commit }) {
        try {
          const response = await fetch("http://127.0.0.1:5000/get/unflagged-sponsor", {
            method: "GET",
            mode: "cors",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Bearer " + localStorage.getItem("jwt"),
            },
          });
          if (response.status === 200) {
            const data = await response.json();
            console.log(data, 'unflagged sponsor fetched');
            commit('setSponsor', data.resource); // Commit to Vuex store
          } else {
            alert("Failed to fetch unflaginfluencer");}
        } catch (error) {
          console.error(error);
        }
      },




    async fetchCampaignsall({ commit }) {
        try {
          const response = await fetch("http://127.0.0.1:5000/get/current-campaigns", {
            method: "GET",
            mode: "cors",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Bearer " + localStorage.getItem("jwt"),
            },
          });
  
          if (response.status === 200) {
            const data = await response.json();
            console.log(data, 'campaigns fetched');
            commit('setCampaigns', data); // Commit to Vuex store
          } else {
            alert("Failed to fetch campaigns");
          }
        } catch (error) {
          console.error(error);
        }
      },

    async fetchFlagInfluencers({ commit }) {
        try {
          const response = await fetch('http://127.0.0.1:5000/get/all/flagged/influencers', {
            method: 'GET',
            credentials: 'include',
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + localStorage.getItem('jwt'),
            },
          });
          if (response.status === 200) {
            const data = await response.json();
            console.log(data, 'flagged influencers fetched');
            commit('setFlagInfluencer', data.resource);
          } else {
            const data = await response.json();
            alert(data.message);
          }
        } catch (error) {
          console.error('Error fetching flagged influencers:', error);
        }
      },

      


    



      async fetchFlagSponsor({ commit }) {
        try {
          const response = await fetch('http://127.0.0.1:5000/get/all/flagged/sponsors', {
            method: 'GET',
            credentials: 'include',
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + localStorage.getItem('jwt'),
            },
          });
          if (response.status === 200) {
            const data = await response.json();
            console.log(data, 'flagged sponsors fetched');
            commit('setFlagSponsor', data.resource);
          } else {
            const data = await response.json();
            alert(data.message);
          }
        } catch (error) {
          console.error('Error fetching flagged sponsors:', error);
        }
      },
      

    async fetchOtherCampaigns({ commit }) {
        try {
            const influencerEmail = localStorage.getItem('email');
            const response = await fetch(`http://127.0.0.1:5000/campaigns/others`, {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt'),
                    'Content-Type': 'application/json',
                    'email': influencerEmail // Pass the influencer email in the headers
                },
            });
    
            if (response.status === 200) {
                const data = await response.json();
                commit('setOtherCamp', data.campaigns); // Store the fetched campaigns in the state
                console.log(data.campaigns);
            } else {
                const data = await response.json();
                alert(data.message);
            }
        } catch (error) {
            console.error(error);
        }
    },
    

    async fetchNotifications({ commit }) {
      try {
        const response = await fetch('http://127.0.0.1:5000/get/notifications', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('jwt'),
            'X-User-Email': localStorage.getItem('email'), // Pass email as a custom header
            'X-User-role': localStorage.getItem('role')
          },
        });
    
        if (response.status === 200) {
          const data = await response.json();
          console.log(data.campaigns, 'notifications fetched');
          commit('setNotifications', data.campaigns);  // Store the fetched notifications in Vuex state
        } else {
          const data = await response.json();
          alert(data.message);  // Handle any error message returned from the backend
        }
      } catch (error) {
        console.log(data)
        console.error('Error fetching notifications:', error);  // More descriptive error message
        alert('Failed to fetch notifications');  // Notify user
      }
    },
    




    async fetchNotifications2({ commit }) {
      try {
        const response = await fetch('http://127.0.0.1:5000/get/notifications2', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('jwt'),
            'X-User-Email': localStorage.getItem('email'), // Pass email as a custom header
            'X-User-role': localStorage.getItem('role')
          },
        });
    
        if (response.status === 200) {
          const data = await response.json();
          console.log(data.campaigns, 'notifications2 fetched');
          commit('setNotifications2', data.campaigns);  // Store the fetched notifications in Vuex state
        } else {
          const data = await response.json();
          alert(data.message);  // Handle any error message returned from the backend
        }
      } catch (error) {
        console.log(data)
        console.error('Error fetching notifications2:', error);  // More descriptive error message
        alert('Failed to fetch notifications2');  // Notify user
      }
    },


    async fetchNotifications3({ commit }) {
      try {
        const response = await fetch('http://127.0.0.1:5000/get/notifications3', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('jwt'),
            'X-User-Email': localStorage.getItem('email'), // Pass email as a custom header
            'X-User-role': localStorage.getItem('role')
          },
        });
    
        if (response.status === 200) {
          const data = await response.json();
          console.log(data.campaigns, 'notifications3 fetched');
          commit('setNotifications3', data.campaigns);  // Store the fetched notifications in Vuex state
        } else {
          const data = await response.json();
          alert(data.message);  // Handle any error message returned from the backend
        }
      } catch (error) {
        console.log(data)
        console.error('Error fetching notifications3:', error);  // More descriptive error message
        alert('Failed to fetch notifications3');  // Notify user
      }
    },












    
    async fetchNotifications1({ commit }) {
      try {
        const response = await fetch('http://127.0.0.1:5000/get/notifications1', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('jwt'),
            'X-User-Email': localStorage.getItem('email'), // Pass email as a custom header
            'X-User-role': localStorage.getItem('role')
          },
        });
    
        if (response.status === 200) {
          const data = await response.json();
          console.log(data.campaigns, 'notifications fetched');
          commit('setNotifications1', data.campaigns);  // Store the fetched notifications in Vuex state
        } else {
          const data = await response.json();
          alert(data.message);  // Handle any error message returned from the backend
        }
      } catch (error) {
        console.log(data)
        console.error('Error fetching notifications1:', error);  // More descriptive error message
        alert('Failed to fetch notifications1');  // Notify user
      }
    },











    async fetchCampaigns({ commit }) {
        try {
          const response = await fetch('http://127.0.0.1:5000/get/campaigns', {
            method: 'GET',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + localStorage.getItem('jwt'),
              'X-User-Email': localStorage.getItem('email'), // Pass email as a custom header
              'X-User-role': localStorage.getItem('role')
            },
          });
      
          if (response.status === 200) {
            const data = await response.json();
            console.log(data.campaigns_list, 'categories fetched');
            commit('setCampaigns', data);
          } else {
            const data = await response.json();
            alert(data.message);
          }
        } catch (error) {
          console.error(error);
        }
      },
      
      










async fetchCompletedCampaigns({ commit }) {
    try {
      const response = await fetch('http://127.0.0.1:5000/complete/campaign', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          withCredentials: true,
          credentials: 'include',
        },
      });
      if (response.status === 200) {
        const data = await response.json();
        console.log(data, 'completed campaigns fetched');
        commit('setCompleCamps', data
        );
      } else {
        const data = await response.json();
        alert(data.message);
      }
    } catch (error) {
      console.error('Error fetching completed campaigns:', error);
    }
  },



//   async markCampaignComplete({ commit }, { campaignId, proof }) {
//     try {
//       const response = await axios.get(
//         `http://127.0.0.1:5000/complete/campaign/${campaignId}?proof=${encodeURIComponent(proof)}`
//       );
//       if (response.status === 200) {
//         commit('updateCompleCamp', response.data);
//         alert('Campaign marked as completed successfully.');
//       }
//     } catch (error) {
//       console.error('Error marking campaign as complete:', error);
//     }
//   },
// },


      async fetchinfluencer({ commit }) {
          try {
              const response = await fetch('http://127.0.0.1:5000/get/influencers', {
                  method: 'GET',
                  headers: {
                      'Content-Type': 'application/json',
                      withCredentials: true,
                      credentials: 'include'
                  },
              });
              if (response.status === 200) {
                  const data = await response.json();
                  console.log(data, 'influencers fetched');
                  commit('setinfluencer', data);
              } else {
                  const data = await response.json();
                  alert(data.message);
              }
          } catch (error) {
              console.error(error);
          }
      },


      async fetchSponsor({ commit }) {
          try {
              const response = await fetch('http://127.0.0.1:5000/get/sponsors', {
                  method: 'GET',
                  headers: {
                      'Content-Type': 'application/json',
                      withCredentials: true,
                      credentials: 'include'
                  },
              });
              if (response.status === 200) {
                  const data = await response.json();
                  console.log(data, 'sponsors fetched');
                  commit('setSponsors', data);
              } else {
                  const data = await response.json();
                  alert(data.message);
              }
          } catch (error) {
              console.error(error);
          }
      },


      async fetchProofs({ commit }) {
          try {
              const response = await fetch('http://127.0.0.1:5000/get/proofs', {
                  method: 'GET',
                  headers: {
                      'Content-Type': 'application/json',
                      withCredentials: true,
                      credentials: 'include'
                  },
              });
              if (response.status === 200) {
                  const data = await response.json();
                  console.log(data, 'proofs fetched');
                  commit('setProofs', data);
              } else {
                  const data = await response.json();
                  alert(data.message);
              }
          } catch (error) {
              console.error(error);
          }
      },



      async fetchIndustries({ commit }) {
          try {
              const response = await fetch('http://127.0.0.1:5000/get/industries', {
                  method: 'GET',
                  headers: {
                      'Content-Type': 'application/json',
                      withCredentials: true,
                      credentials: 'include'
                  },
              });
              if (response.status === 200) {
                  const data = await response.json();
                  console.log(data, 'industries fetched');
                  commit('setIndustries', data);
              } else {
                  const data = await response.json();
                  alert(data.message);
              }
          } catch (error) {
              console.error(error);
          }
      },


      async fetchAuthenticatedUsers({ commit }) {
          try {
              const response = await fetch('http://127.0.0.1:5000/get/authenticated-users', {
                  method: 'GET',
                  headers: {
                      'Content-Type': 'application/json',
                      withCredentials: true,
                      credentials: 'include'
                  },
              });
              if (response.status === 200) {
                  const data = await response.json();
                  console.log(data, 'authenticated users fetched');
                  commit('setAuthenticatedUser', data);
              } else {
                  const data = await response.json();
                  alert(data.message);
              }
          } catch (error) {
              console.error(error);
          }
      },


      async fetchAccepCamps({ commit }) {
          try {
              const response = await fetch('http://127.0.0.1:5000/get/accep-camps', {
                  method: 'GET',
                  headers: {
                      'Content-Type': 'application/json',
                      withCredentials: true,
                      credentials: 'include'
                  },
              });
              if (response.status === 200) {
                  const data = await response.json();
                  console.log(data, 'accepted campaigns fetched');
                  commit('setAccepCamps', data);
              } else {
                  const data = await response.json();
                  alert(data.message);
              }
          } catch (error) {
              console.error(error);
          }
      },



      async fetchCompleCamps({ commit }) {
          try {
              const response = await fetch('http://127.0.0.1:5000/get/comple-camps', {
                  method: 'GET',
                  headers: {
                      'Content-Type': 'application/json',
                      withCredentials: true,
                      credentials: 'include'
                  },
              });
              if (response.status === 200) {
                  const data = await response.json();
                  console.log(data, 'completed campaigns fetched');
                  commit('setCompleCamps', data);
              } else {
                  const data = await response.json();
                  alert(data.message);
              }
          } catch (error) {
              console.error(error);
          }
      },


      async fetchSpoCamps({ commit }) {
          try {
              const response = await fetch('http://127.0.0.1:5000/get/spo-camps', {
                  method: 'GET',
                  headers: {
                      'Content-Type': 'application/json',
                      withCredentials: true,
                      credentials: 'include'
                  },
              });
              if (response.status === 200) {
                  const data = await response.json();
                  console.log(data, 'sponsored campaigns fetched');
                  commit('setSpoCamps', data);
              } else {
                  const data = await response.json();
                  alert(data.message);
              }
          } catch (error) {
              console.error(error);
          }
      }
    }
    
});

export default store;
