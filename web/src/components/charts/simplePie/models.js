export const simplePieOptions = {
  chart: {
    type: "donut",
    width: 360,
  },
  legend: {
    position: "bottom",
    fontFamily: "Geologica Cursive",
    fontSize: "16px",
  },
  colors: ["#0BA360", "#005BEA", "#FF9A9E", "#F6D365", "#0BA360", "#005BEA", "#FF9A9E", "#F6D365", "#0BA360", "#005BEA", "#FF9A9E", "#F6D365", "#0BA360", "#005BEA", "#FF9A9E", "#F6D365"],
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
      gradientToColors: ["#3CBA92", "#00C6FB", "#FECFEF", "#FDA085", "#0BA360", "#005BEA", "#FF9A9E", "#F6D365", "#0BA360", "#005BEA", "#FF9A9E", "#F6D365", "#0BA360", "#005BEA", "#FF9A9E", "#F6D365"],
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
  ],
};
