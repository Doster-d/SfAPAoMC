export const simplePieOptions = {
  chart: {
    type: "donut",
    width: 360,
  },
  legend: {
    //showsForZeroSeries: true,
    position: "bottom",
    fontFamily: "Geologica Cursive",
    fontSize: "16px",
  },
  colors: ["#F6D365", "#F093FB", "#50CC7F", "#6A11CB", "#0BA360", "#7028E4", "#F83600", "#6E45E2", "#F77062", "#FF057C", "#4FACFE", "#43E97B", "#F78CA0", "#C471F5", "#434343", "#C79081", "#09203F"],
  labels: [
    "ВУЗ",
    "Высокотехнологичные ИТ компании",
    "Добывающая промышленность",
    "Здравоохранение и социальные услуги",
    "Колледжи",
    "Медиа и развлечения",
    "Научные организации",
    "Нет категории",
    "Обрабатывающая промышленность",
    "Розничная торговля",
    "Сельское хозяйство и пищевая промышленность",
    "Строительство и недвижимость",
    "Транспорт и логистика",
    "Туризм и гостиничный бизнес",
    "Финансовые услуги",
    "Энергетика",
    "Юридические и профессиональные услуги"
  ],
  fill: {
    type: "gradient",
    gradient: {
      shade: "light",
      type: "horizontal",
      shadeIntensity: 0.5,
      gradientToColors: ["#FDA085", "#F5576C", "#F5D100", "#2575FC", "#3CBA92", "#E5B2CA", "#F9D423", "#88D3CE", "#FE5196", "#321575", "#00F2FE", "#38F9D7", "#FD868C", "#000000", "#DFA579", "#537895"],
      inverseColors: true,
      opacityFrom: 1,
      opacityTo: 1,
      stops: [20, 100],
    },
  },
  plotOptions: {
    pie: {
      dataLabels: {
        show: false,
      },
      donut: {
        size: "65%",
        labels: {
          show: false,
        },
      },
    },
  },
  dataLabels: {
    enabled: false,
  },
  responsive: [
    {
      breakpoint: 1023,
      options: {
        chart: {
          width: 380,
        },
      },
    },
    {
      breakpoint: 425,
      options: {
        chart: {
          width: 320,
        },
      },
    },
  ],
};
