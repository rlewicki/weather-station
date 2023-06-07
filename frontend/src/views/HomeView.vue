<script setup lang="ts">
import LineChart from '../components/LineChart.vue'
import { ref, watchEffect } from 'vue';

const API_URL = "http://localhost:8080/api/v1/sampleReading/"
const API_LAST_COUNT = "last_count?count=7"
const API_LAST = "last"

let chart_data_loaded = ref(false)
let labels: string[] = []
let temperature_samples: number[] = []
let humidity_samples: number[] = []
let current_inside_temperature = 0
let current_inside_humidity = 0
const response = ref(null)
watchEffect(async () => {
  response.value = await (await fetch(API_URL + API_LAST_COUNT)).json()
  for (let i = 0; i < response.value.length; i++) {
    labels.push(getHourAndMinuteFromDate(response.value[i].date))
    temperature_samples.push(response.value[i].temperature)
    humidity_samples.push(response.value[i].humidity)
  }

  response.value = await (await fetch(API_URL + API_LAST)).json()
  current_inside_temperature = response.value.temperature
  current_inside_humidity = response.value.humidity

  chart_data_loaded.value = true
})

function getHourAndMinuteFromDate(date: string) {
  return date.substring(11, 16)
}

function getYearFromDate(date: string) {
  return date.substring(0, 4)
}

function getMonthFromDate(date: string) {
  return date.substring(5, 7)
}

function getDayFromDate(date: string) {
  return date.substring(8, 10)
}
</script>

<template>
  <main>
    <div class="row row-cols-1 row-cols-md-3 mb-3 text-center">
      <div class="col">
        <div class="card mb-4 rounded-3 shadow-sm">
          <div class="card-header py-3">
            <h4 class="my-0 fw-normal">Inside</h4>
          </div>
          <div class="card-body">
            <section v-if="chart_data_loaded">
              <h1>Current</h1>
              <h2>{{ current_inside_temperature }}°C</h2>
              <h2>{{ current_inside_humidity }}%</h2>
              <LineChart
                id="inside_temp" 
                title="Temperature"
                value-title="Temperature level"
                :labels="labels" 
                :samples="temperature_samples" 
                :min-reading-offset="2" 
                :max-reading-offset="2"
                chart-color="#B31312"/>
              <LineChart
                id="inside_himidity" 
                title="Humidity" 
                :labels="labels" 
                :samples="humidity_samples"
                value-title="Humidity level"
                :min-reading-offset="10"
                :max-reading-offset="10"
                chart-color="#A1C298"/>
            </section>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card mb-4 rounded-3 shadow-sm">
          <div class="card-header py-3">
            <h4 class="my-0 fw-normal">Wrocław</h4>
          </div>
          <div class="card-body">
            <section v-if="chart_data_loaded">
              <h1>Current</h1>
              <h2>TBD</h2>
              <h2>TBD</h2>
            </section>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card mb-4 rounded-3 shadow-sm">
          <div class="card-header py-3">
            <h4 class="my-0 fw-normal">Berlin</h4>
          </div>
          <div class="card-body">
            <section v-if="chart_data_loaded">
              <h1>Current</h1>
              <h2>TBD</h2>
              <h2>TBD</h2>
            </section>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
