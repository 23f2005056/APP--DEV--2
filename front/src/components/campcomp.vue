<template>
  <div class="row justify-content-center m-3 text-color-light">
    <div class="card bg-light" style="width: 18rem;">
      <div class="card-body">
        <div class="d-flex justify-content-end">
          <!-- Cross button to close the card -->
          <button type="button" class="btn-close" aria-label="Close" @click="closeCard"></button>
        </div>
        <h5 class="card-title">Campaign Completion</h5>
        <form @submit.prevent="submitProof">
          <div class="mb-3">
            <label for="proof" class="form-label">Proof</label>
            <textarea 
              id="proof" 
              class="form-control" 
              v-model="proofText" 
              rows="4" 
              placeholder="Write proof of campaign completion..." 
              required
            ></textarea>
            <div v-if="message" class="alert alert-warning mt-2">
              {{ message }}
            </div>
          </div>
          <div class="d-flex">
            <button type="submit" class="btn btn-outline-primary me-5">Submit</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      proofText: '', // To hold the written proof
      message: ''
    };
  },
  methods: {
    async submitProof() {
      if (!this.proofText.trim()) {
        this.message = 'Proof cannot be empty.';
        return;
      }

      const payload = {
        proof: this.proofText
      };

      try {
        const response = await fetch(`http://127.0.0.1:5000/influ/camp/comp/${this.$route.params.id}`, {
          method: 'POST',
          mode: 'cors',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('jwt')
          },
          body: JSON.stringify(payload)
        });

        if (response.status === 200) {
          this.message = 'Campaign completed successfully!';
        } else {
          this.message = 'An error occurred.';
        }
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style>
.text-color-light {
  color: #6c757d; /* Adjust this based on your theme */
}
</style>
