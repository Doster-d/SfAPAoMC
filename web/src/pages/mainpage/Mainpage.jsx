import { Link } from "react-router-dom";
import "./style.scss";

// Import Swiper styles
import "swiper/css";
import TeamSlider from "../../components/teamSlider/TeamSlider";
import { useEffect, useState } from "react";
import MultiRadialBar from "../../components/charts/multiRadialBar/MultiRadialBar";
import SemiRadialBar from "../../components/charts/semiRadialBar/SemiRadialBar";
import TablePie from "../../components/charts/tablePie/TablePie";
function Mainpage() {
  const [barSelected, setBarSelected] = useState(undefined);
  useEffect(() => {
    console.log(barSelected);
  }, [barSelected]);
  const handleBarSelection = (event) => {
    if (event.target.parentElement.attributes.seriesName) {
      if (event.target.attributes.selected.value === "true") {
        setBarSelected(event.target.parentElement.attributes.seriesName.value);
      } else {
        setBarSelected(undefined);
      }
    }
  };

  return (
    <main className="main">
      <section className="main-banner">
        <div className="container">
          <h1 className="main-banner__title title-h1">
            Решение кейса “Сервис анализа патентной активности компаний Москвы”
          </h1>
          <Link className="main-banner__button">я фурри фашист </Link>
        </div>
      </section>
      <TeamSlider />
      <section className="charts">
        <h2 className="title-h2 charts__title">ОБЩАЯ СТАТИСТИКА</h2>
        <div className="container charts__container">
          <div className="charts__main-chart">
            <MultiRadialBar handleBarSelection={handleBarSelection} series={[100, 90, 80]} />
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
  );
}

export default Mainpage;
