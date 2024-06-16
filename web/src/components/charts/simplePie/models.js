export const simplePieOptions = {
    chart: {
      type: "donut",
      width: 360
    },
    legend: {
      position: "bottom",
      fontFamily: 'Geologica Cursive',
      fontSize: '16px',

    },
    colors: ['#0BA360', '#005BEA', '#FF9A9E', '#F6D365'],
    labels: ["Label 1", "Label 2", "Label 3", "Label 4"],
    fill: {
      type: 'gradient',
      gradient: {
        shade: 'light',
        type: "horizontal",
        shadeIntensity: 0.5,
        gradientToColors: ['#3CBA92', '#00C6FB', '#FECFEF', '#FDA085'],
        inverseColors: true,
        opacityFrom: 1,
        opacityTo: 1,
        stops: [20, 100],
      }
    },
    plotOptions: {
      pie: {
        dataLabels: {
          show: false,
        },
        donut: {
          size: '65%',
          labels: {
            show: false
          }
        }
      }
    },
    dataLabels: {
      enabled: false,
    },
    responsive: [{
        breakpoint: 1023,
        options: {
          chart: {
            width: 380
          },
        }
      }]
  };