<script setup lang="ts">
import LineChart from '../components/LineChart.vue'
import { ref, watchEffect } from 'vue';

let loaded = ref(false)
let labels: string[] = []
let temperature_samples: number[] = []
let humidity_samples: number[] = []

const response = ref(null)
watchEffect(async () => {
  response.value = await (await fetch("http://localhost:8080/api/v1/sampleReading/last_count?count=50")).json()
  for (let i = 0; i < response.value.length; i++) {
    labels.push(response.value[i].date)
    temperature_samples.push(response.value[i].temperature)
    humidity_samples.push(response.value[i].humidity)
  }
  loaded.value = true
})
</script>

<template>
  <main>
    <section v-if="loaded">
      <LineChart
        id="inside_temp" 
        title="Inside Temperature"
        value-title="Temperature level"
        :labels="labels" 
        :samples="temperature_samples" 
        :min-reading-offset="2" 
        :max-reading-offset="2"
        chart-color="#B31312"/>
      <LineChart
        id="inside_himidity" 
        title="Inside Humidity" 
        :labels="labels" 
        :samples="humidity_samples"
        value-title="Humidity level"
        :min-reading-offset="10"
        :max-reading-offset="10"
        chart-color="#A1C298"/>
    </section>
    <!-- <div class="row row-cols-1 row-cols-md-3 mb-3 text-center">
      <div class="col">
        <div class="card mb-4 rounded-3 shadow-sm">
          <div class="card-header py-3">
            <h4 class="my-0 fw-normal">Free</h4>
          </div>
          <div class="card-body">
            <h1 class="card-title pricing-card-title">$0<small class="text-body-secondary fw-light">/mo</small></h1>
            <ul class="list-unstyled mt-3 mb-4">
              <li>10 users included</li>
              <li>2 GB of storage</li>
              <li>Email support</li>
              <li>Help center access</li>
            </ul>
            <button type="button" class="w-100 btn btn-lg btn-outline-primary">Sign up for free</button>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card mb-4 rounded-3 shadow-sm">
          <div class="card-header py-3">
            <h4 class="my-0 fw-normal">Pro</h4>
          </div>
          <div class="card-body">
            <h1 class="card-title pricing-card-title">$15<small class="text-body-secondary fw-light">/mo</small></h1>
            <ul class="list-unstyled mt-3 mb-4">
              <li>20 users included</li>
              <li>10 GB of storage</li>
              <li>Priority email support</li>
              <li>Help center access</li>
            </ul>
            <button type="button" class="w-100 btn btn-lg btn-primary">Get started</button>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card mb-4 rounded-3 shadow-sm border-primary">
          <div class="card-header py-3 text-bg-primary border-primary">
            <h4 class="my-0 fw-normal">Enterprise</h4>
          </div>
          <div class="card-body">
            <h1 class="card-title pricing-card-title">$29<small class="text-body-secondary fw-light">/mo</small></h1>
            <ul class="list-unstyled mt-3 mb-4">
              <li>30 users included</li>
              <li>15 GB of storage</li>
              <li>Phone and email support</li>
              <li>Help center access</li>
            </ul>
            <button type="button" class="w-100 btn btn-lg btn-primary">Contact us</button>
          </div>
        </div>
      </div>
    </div> -->
    <!-- <LineChart2 /> -->
  </main>
</template>
