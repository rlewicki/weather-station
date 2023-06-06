<template>
  <div>
    <canvas :id="id"></canvas>
  </div>
</template>
  
<script setup lang="ts">
import Chart, { Colors, registerables } from 'chart.js/auto'
import { onMounted } from 'vue';

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

let maxSample = -999999;
let minSample = 9999999;
for (var sample of props.samples) {
  if (sample < minSample) {
    minSample = sample;
  }

  if (sample > maxSample) {
    maxSample = sample;
  }
}

const data = {
  labels: props.labels,
  datasets: [{
    label: "Dataset",
    data: props.samples,
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
  