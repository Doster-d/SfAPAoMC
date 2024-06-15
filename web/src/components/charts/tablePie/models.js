export const optionsPie = {
    chart: {
      width: 397,
      type: "donut",
    },
    plotOptions: {
      pie: {
        startAngle: 0,
        endAngle: 360,
        donut: {
          background: "transparent",
          labels: {
            show: true,
            name: {
              offsetY: -20,
            },
            value: {
              show: true,
              color: "#000000",
              fontSize: "48px",
              fontFamily: "Geologica Cursive",
              fontWeight: 500,
            },
            total: {
              show: true,
              showAlways: true,
              label: `Всего`,
              color: "#737373",
              fontSize: "24px",
              fontFamily: "Geologica Cursive",
              fontWeight: 500,
              formatter: function (w) {
                return w.globals.seriesTotals.reduce((a, b) => {
                  return a + b;
                }, 0);
              },
            },
          },
        },
      },
      total: {
        show: true,
        showAlways: true,
        label: "Total",
        fontSize: "22px",
        fontFamily: "Helvetica, Arial, sans-serif",
        fontWeight: 600,
        color: "#373d3f",
        formatter: function (w) {
          return w.globals.seriesTotals.reduce((a, b) => {
            return a + b;
          }, 0);
        },
      },
    },
    dataLabels: {
      enabled: false,
    },
    fill: {
      type: "gradient",
      gradient: {
        shade: "light",
        type: "horizontal",
        gradientToColors: ["#00C6FB", "#F9D423", "#00E3AE"],
        shadeIntensity: 0.4,
        inverseColors: true,
        opacityFrom: 1,
        opacityTo: 1,
        stops: [30, 100],
      },
    },
    legend: {
      show: false,
    },
    width: "auto",
    colors: ["#005BEA", "#F83600", "#9BE15D"],
    labels: ["Юридическое лицо", "Инд. предприниматель", "Физическое лицо"],
  };