export const optionsSemiRadial = {
  chart: {
    type: "radialBar",
    offsetY: 0,
    sparkline: {
      enabled: true,
    },
  },
  plotOptions: {
    radialBar: {
      startAngle: -90,
      endAngle: 90,
      hollow: {
        size: "62%",
      },
      track: {
        background: "#F3F3F3",
        strokeWidth: "100%",
        margin: 5, // margin is in pixels
      },
      dataLabels: {
        name: {
          show: true,
          fontSize: "24px",
          fontFamily: "Geologica Cursive",
          fontWeight: 500,
          color: "#737373",
          offsetY: 0,
        },
        value: {
          offsetY: -60,
          fontSize: "48px",
          fontFamily: "Geologica Cursive",
          fontWeight: 500,
          color: "#000000",
        },
      },
    },
  },
  fill: {
    type: "gradient",
    gradient: {
      gradientToColors: ["#00F2FE"],
      shadeIntensity: 0.4,
      inverseColors: true,
      opacityFrom: 1,
      opacityTo: 1,
      stops: [0, 100],
    },
  },
  labels: ["Размеченных патента"],
  colors: ["#4FACFE"],
};
