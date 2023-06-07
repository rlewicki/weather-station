<template>
  <div>
    <canvas :id="id"></canvas>
  </div>
</template>
  
<script setup lang="ts">
import Chart, { Colors, registerables } from 'chart.js/auto'
import { onMounted, computed } from 'vue';

console.log("beginning of line chart component")

const props = defineProps<{
  id: string,
  title: string,
  valueTitle: string,
  labels: Array<string>,
  samples: Array<number>,
  minReadingOffset: number,
  maxReadingOffset: number,
  chartColor: string,
}>()

const chartSamples = computed(() => props.samples)

let maxSample = -999999;
let minSample = 9999999;
for (var sample of chartSamples.value) {
  if (sample < minSample) {
    minSample = sample;
  }

  if (sample > maxSample) {
    maxSample = sample;
  }
}

console.log("Chart title: " + props.title)
console.log("Chart labels: ")
console.log(props.labels)
console.log("Chart samples: ")
console.log(chartSamples)

const data = {
  labels: props.labels,
  datasets: [{
    label: "Dataset",
    data: chartSamples.value,
    fill: false,
    cubicInterpolationMode: 'monotone',
    tension: 0.4,
    borderColor: props.chartColor,
  }]
}
const options = {
  responsive: true,
  plugins: {
    title: {
      display: true,
      text: props.title
    },
  },
  interaction: {
    intersect: false,
  },
  scales: {
    y: {
      display: true,
      title: {
        display: true,
        text: props.valueTitle
      },
      suggestedMin: minSample - <number>props.minReadingOffset,
      suggestedMax: maxSample + <number>props.maxReadingOffset
    }
  }
}

onMounted(() => {
  const ctx = document.getElementById(props.id);
  new Chart(ctx, 
  {
    type: 'line',
    data: data,
    options: options
  });
})
</script>
  