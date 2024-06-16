import { Link } from "react-router-dom";
import "./style.scss";

// Import Swiper styles
import "swiper/css";
import TeamSlider from "../../components/teamSlider/TeamSlider";
import { useState } from "react";
import MultiRadialBar from "../../components/charts/multiRadialBar/MultiRadialBar";
import SemiRadialBar from "../../components/charts/semiRadialBar/SemiRadialBar";
import TablePie from "../../components/charts/tablePie/TablePie";
import { Helmet } from "react-helmet-async";
function Mainpage() {
  const [barSelected, setBarSelected] = useState(undefined);
  const handleBarSelection = (event) => {
    if (
      event.target.parentElement.attributes.seriesName ||
      event.target.attributes.selected
    ) {
      if (event.target.attributes.selected?.value === "true") {
        setBarSelected(event.target.parentElement.attributes.seriesName?.value);
      } else {
        setBarSelected(undefined);
      }
    }
  };

  return (
    <>
      <Helmet>
        <title>K1 - Анализ патентов</title>
        <meta
          name="description"
          content="Сервис анализа патентной активности компаний Москвы: мониторинг, анализ и визуализация патентов."
        />
        <meta rel="canonical" href="/"/>
      </Helmet>
      <main className="main">
        <section className="main-banner">
          <div className="container">
            <h1 className="main-banner__title title-h1">
              Решение кейса “Сервис анализа патентной активности компаний
              Москвы”
            </h1>
            <Link className="main-banner__button">Кнопка для чего-то</Link>
          </div>
        </section>
        <TeamSlider />
        <section className="charts">
          <h2 className="title-h2 charts__title">ОБЩАЯ СТАТИСТИКА</h2>
          <div className="container charts__container">
            <div className="charts__main-chart">
              <MultiRadialBar
                handleBarSelection={handleBarSelection}
                series={[100, 90, 80]}
              />
            </div>
            {barSelected && (
              <div className="charts__additional-charts">
                <SemiRadialBar series={[72]} />
                <TablePie series={[28, 12, 6]} />
              </div>
            )}
          </div>
        </section>
      </main>
    </>
  );
}

export default Mainpage;
