let myChart;

const predefinedColors = [
  'rgba(255, 99, 132, 0.2)',
  'rgba(54, 162, 235, 0.2)',
  'rgba(255, 206, 86, 0.2)',
  'rgba(75, 192, 192, 0.2)',
  'rgba(153, 102, 255, 0.2)',
  'rgba(255, 159, 64, 0.2)',
  'rgba(199, 199, 199, 0.2)',
  'rgba(255, 99, 71, 0.2)',
  'rgba(60, 179, 113, 0.2)',
  'rgba(106, 90, 205, 0.2)',
  'rgba(255, 140, 0, 0.2)',
  'rgba(70, 130, 180, 0.2)',
  'rgba(244, 164, 96, 0.2)',
  'rgba(32, 178, 170, 0.2)',
  'rgba(218, 112, 214, 0.2)',
  'rgba(255, 215, 0, 0.2)',
  'rgba(0, 191, 255, 0.2)',
  'rgba(255, 69, 0, 0.2)',
  'rgba(34, 139, 34, 0.2)',
  'rgba(138, 43, 226, 0.2)'
];

const renderChart = (data, labels) => {
  console.log("Rendering chart with data:", data, "and labels:", labels);
  const colors = predefinedColors.slice(0, labels.length);
  const borderColors = colors.map(color => color.replace('0.2', '1'));
  var ctx = document.getElementById("myChart").getContext("2d");
  if (myChart) {
    myChart.destroy();
  }
  myChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Last 6 months expenses",
          data: data,
          backgroundColor: colors,
          borderColor: borderColors,
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Expenses per category",
      },
    },
  });
};

const getChartData = () => {
  console.log("Fetching chart data");
  fetch("/expense_category_summary")
    .then((res) => {
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      return res.json();
    })
    .then((results) => {
      console.log("Results from API:", results);
      const category_data = results.expense_category_data;
      console.log("Category data:", category_data);
      const labels = Object.keys(category_data);
      const data = Object.values(category_data);
      console.log("Labels:", labels);
      console.log("Data:", data);

      if (labels.length === 0 || data.length === 0) {
        console.log("No data available to display.");
        document.getElementById("myChart").style.display = "none";
        document.getElementById("noDataMessage").style.display = "block";
      } else {
        renderChart(data, labels);
      }
    })
    .catch((error) => {
      console.error("Error fetching chart data:", error);
      document.getElementById("noDataMessage").innerText = `Error: ${error.message}`;
      document.getElementById("noDataMessage").style.display = "block";
    });
};

document.addEventListener("DOMContentLoaded", getChartData);

document.getElementById("expenses-summary-link").addEventListener("click", (event) => {
  event.preventDefault();
  getChartData();
});
