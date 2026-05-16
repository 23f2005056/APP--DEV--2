<template>
    <div class="row justify-content-center m-3 text-color-light">
      <div class="card bg-light" style="width: 36rem;">
        <div class="card-body">
          <h5 class="card-title text-center">Campaign Statistics</h5>
          <div class="d-grid gap-3 mt-4">
            <button class="btn btn-outline-primary" @click="getStats">Get Stats</button>
            <button class="btn btn-outline-success" @click="downloadStats">Download Stats</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      getStats() {
        // Define the route for "Get Stats"
        const url = "http://127.0.0.1:5000/get/report/data";
        window.open(url, "_blank");
      },
      downloadStats() {
        // Define the route for "Download Stats"
        const url = "http://127.0.0.1:5000/get/report/download";
        window.open(url, "_blank");
      }
    }
  }
  </script>

  