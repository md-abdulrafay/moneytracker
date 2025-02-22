let myChart;
let weeklyChart;
let yearlyChart;

const getRandomType = () => {
  const types = [
    "bar",
    "horizontalBar",
    "pie",
    "line",
    "radar",
    "doughnut",
    "polarArea",
    "doughnut",
  ];
  return types[Math.floor(Math.random() * types.length)];
};

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

const displayChart = (data, labels) => {
  const type = getRandomType();
  const colors = predefinedColors.slice(0, labels.length);
  const borderColors = colors.map(color => color.replace('0.2', '1'));
  var ctx = document.getElementById("myChart").getContext("2d");
  if (myChart) {
    myChart.destroy();
  }
  myChart = new Chart(ctx, {
    type: type, // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data: {
      labels: labels,
      datasets: [
        {
          data: data,
          backgroundColor: colors,
          borderColor: borderColors,
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: false,
      },
      legend: {
        display: true,
        position: "right",
        labels: {
          fontColor: "#000",
        },
      },
    },
  });
};

const displayWeeklyChart = (data, labels) => {
  var ctx = document.getElementById("weeklyChart").getContext("2d");
  if (weeklyChart) {
    weeklyChart.destroy();
  }
  weeklyChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Weekly Expenses',
          data: data,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: 'Expenses Over This Week',
        fontSize: 20,
      },
      scales: {
        xAxes: [{
          type: 'category',
          labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        }]
      },
      legend: {
        display: true,
        position: 'right',
        labels: {
          fontColor: '#000',
        },
      },
    },
  });
};

const displayYearlyChart = (data, labels) => {
  var ctx = document.getElementById("yearlyChart").getContext("2d");
  if (yearlyChart) {
    yearlyChart.destroy();
  }
  yearlyChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Yearly Expenses',
          data: data,
          backgroundColor: 'rgba(255, 159, 64, 0.2)',
          borderColor: 'rgba(255, 159, 64, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: 'Expenses Over This Year',
        fontSize: 20,
      },
      scales: {
        xAxes: [{
          type: 'category',
          labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        }]
      },
      legend: {
        display: true,
        position: 'right',
        labels: {
          fontColor: '#000',
        },
      },
    },
  });
};

const getCategoryData = () => {
  console.log("Fetching chart data");
  fetch("/expense_category_summary/")
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
        displayChart(data, labels);
      }

      const weeklyData = results.weekly_expense_data;
      const weeklyLabels = Object.keys(weeklyData);
      const weeklyValues = Object.values(weeklyData);

      if (weeklyLabels.length === 0 || weeklyValues.length === 0) {
        console.log("No weekly data available to display.");
        document.getElementById("weeklyChart").style.display = "none";
        document.getElementById("noWeeklyDataMessage").style.display = "block";
      } else {
        displayWeeklyChart(weeklyValues, weeklyLabels);
      }

      const yearlyData = results.yearly_expense_data;
      const yearlyLabels = Object.keys(yearlyData);
      const yearlyValues = Object.values(yearlyData);

      if (yearlyLabels.length === 0 || yearlyValues.length === 0) {
        console.log("No yearly data available to display.");
        document.getElementById("yearlyChart").style.display = "none";
        document.getElementById("noYearlyDataMessage").style.display = "block";
      } else {
        displayYearlyChart(yearlyValues, yearlyLabels);
      }
    })
    .catch((error) => {
      console.error("Error fetching chart data:", error);
      document.getElementById("noDataMessage").innerText = `Error: ${error.message}`;
      document.getElementById("noDataMessage").style.display = "block";
    });
};

document.addEventListener("DOMContentLoaded", getCategoryData);

document.getElementById("expenses-summary-link").addEventListener("click", (event) => {
  event.preventDefault();
  getCategoryData();
});
