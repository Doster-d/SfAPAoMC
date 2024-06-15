

export const getOptionsMultiRadial = (handleBarSelection) => ({
    chart: {
      height: 390,
      type: "radialBar",
      events: {
        click: (event) => {
          handleBarSelection(event);
        },
      },
    },
    plotOptions: {
      radialBar: {
        endAngle: 270,
        hollow: {
          size: "55%",
        },
        track: {
          show: false,
        },
        dataLabels: {
          name: {
            show: false,
          },
          value: {
            show: false,
          },
        },
        barLabels: {
          enabled: true,
          useSeriesColors: false,
          margin: 4,
          fontSize: "24px",
          fontFamily: "Geologica",
          color: "#737373",
          formatter: function (seriesName, opts) {
            return (
              seriesName + " " + opts.w.globals.series[opts.seriesIndex] + "%"
            );
          },
        },
      },
    },
    fill: {
      type: "gradient",
      gradient: {
        shade: "dark",
        type: "vertical",
        shadeIntensity: 0.5,
        gradientToColors: ["#3CBA92", "#16D9E3", "#F9D423"],
        inverseColors: false,
        opacityFrom: 1,
        opacityTo: 1,
        stops: [0, 100],
      },
    },
    colors: ["#0BA360", "#46AEF7", "#F83600"],
    labels: ["Модель", "Образец", "Изобретение"],
  })
