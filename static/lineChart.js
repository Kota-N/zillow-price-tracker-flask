const ctx = document.getElementById('line-chart').getContext('2d');

// fetch('http://127.0.0.1:5000/api/houses').then(res => res.json()).then(data => console.log(data));
// fetch('http://127.0.0.1:5000/api/prices').then(res => res.json()).then(data => console.log(data));
// fetch('http://127.0.0.1:5000/api/dates').then(res => res.json()).then(data => console.log(data));
// fetch('http://127.0.0.1:5000/api/prices/1').then(res => res.json()).then(data => console.log(data));

// remove everything but dot
// Number(currency.replace(/[^0-9.-]+/g,""));

const getRandomRGB = () => {
  r = Math.floor(Math.random() * 200) + 40;
  g = Math.floor(Math.random() * 200) + 40;
  b = Math.floor(Math.random() * 200) + 40;

  return `rgb(${r}, ${g}, ${b})`;
};

// Fetches
const fetchHouseData = async () => {
  const res = await fetch('http://127.0.0.1:5000/api/houses');
  const data = await res.json();
  return data;
};

const fetchPriceData = async () => {
  const res = await fetch('http://127.0.0.1:5000/api/prices');
  const data = await res.json();
  return data;
};

const fetchDateData = async () => {
  const res = await fetch('http://127.0.0.1:5000/api/dates');
  const data = await res.json();
  return data;
};

// ----------------------------------------------
// Functions to build chart data
// ----------------------------------------------
const buildChartLabels = dateData => {
  const labels = [];
  for (let i = 0; i < dateData.length; i++) {
    labels.push(dateData[i]['date']);
  }
  return labels;
};

// function for buildDatasets() --------------------------->
const buildDatasetsData = async (dateData, houseId) => {
  const res = await fetch('http://127.0.0.1:5000/api/prices/' + houseId);
  const priceDataById = await res.json();

  datasetsData = [];

  for (let i = 0; i < dateData.length; i++) {
    if (priceDataById[0]) {
      if (dateData[i]['date'] === priceDataById[0]['scraped_date']) break;
      else datasetsData.push(undefined);
    }
  }

  for (let i = 0; i < priceDataById.length; i++) {
    datasetsData.push(priceDataById[i]['price'].replace(/[^0-9.-]+/g, ''));
  }
  return datasetsData;
};
// <---------------------------------------------------------

const buildDatasets = async (houseData, dateData) => {
  const datasets = [];

  for (let i = 0; i < houseData.length; i++) {
    const houseId = houseData[i]['id'];
    const data = await buildDatasetsData(dateData, houseId);
    const config = {
      data,
      label: houseData[i]['name'],
      borderColor: getRandomRGB(),
      fill: false,
    };
    datasets.push(config);
  }

  return datasets;
};

// put them together
const buildChartData = async () => {
  const houseData = await fetchHouseData();
  const dateData = await fetchDateData();

  const labels = buildChartLabels(dateData);
  const datasets = await buildDatasets(houseData, dateData);

  return { labels, datasets };
};

// {
//   labels: [],
//   datasets: [
//     {
//       data: [],
//       label: '1',
//       borderColor: "",
//       fill: false
//     },
//   ]
// }

const initChart = async () => {
  const data = await buildChartData();

  const myChart = new Chart(ctx, {
    type: 'line',
    data,
    options: {
      title: {
        display: true,
        text: 'House Prices (zillow.com)',
      },
    },
  });
};

initChart();
