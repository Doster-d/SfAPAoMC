import { Swiper, SwiperSlide } from "swiper/react";
import AV from "./../../assets/images/mainpage/team__vagulich.png";
import figma from "./../../assets/images/mainpage/team_figma.svg";
import js from "./../../assets/images/mainpage/team_js.svg";
import ai from "./../../assets/images/mainpage/team_ai.svg";
import fedorov from "./../../assets/images/mainpage/team_fedorov-new.jpg";
import alekseev from "./../../assets/images/mainpage/team_alekseev-new.jpg";
import savchenko from "./../../assets/images/mainpage/team_savchenko.png";
import arefev from "./../../assets/images/mainpage/team_arefev.png";
import gc from "./../../assets/images/mainpage/team_gc.svg";
import postgre from "./../../assets/images/mainpage/team_postgre.svg";
import react from "./../../assets/images/mainpage/team_react.svg";
import python from "./../../assets/images/mainpage/team_python.svg";
import fastApi from "./../../assets/images/mainpage/team_fastAPI.svg";
import "./style.scss";
import TeamCard from "./components/teamCard/TeamCard";
import { Autoplay, Navigation } from "swiper/modules";
import 'swiper/scss/navigation';
function TeamSlider() {
  return (
    <section className="team">
      <div className="container">
        <h2 className="title-h2 team__title">Команда</h2>
        <Swiper spaceBetween={150} modules={[Navigation, Autoplay]} autoplay={{delay: 3000, disableOnInteraction: true, }} speed={1000} navigation className="team__swiper">
          <SwiperSlide className="team__slide">
            <TeamCard
              avatar={AV}
              avatarAlt={"Alexandr Vagulich"}
              title={"Вагулич Александр"}
              position={"Тимлид, дизайнер"}
              age={"19 лет"}
              description={
                "Сотрудник СНО ИТУ РТУ МИРЭА, стример, а веб-дизайн для души"
              }
            >
              <picture
                className="image-wrapper team-card__floating-image"
                style={{ bottom: "35px", right: "283px" }}
              >
                <img src={figma} alt="Figma" className="image-wrapper__image" />
              </picture>
              <picture
                className="image-wrapper team-card__floating-image"
                style={{ bottom: "20px", right: "119px" }}
              >
                <img
                  src={js}
                  alt="JavaScript"
                  className="image-wrapper__image"
                />
              </picture>
              <picture
                className="image-wrapper team-card__floating-image"
                style={{ top: "0px", right: "0px" }}
              >
                <img src={ai} alt="Ai" className="image-wrapper__image" />
              </picture>
            </TeamCard>
          </SwiperSlide>
          <SwiperSlide className="team__slide">
            <TeamCard
              avatar={fedorov}
              avatarAlt={"Alexandr Fedorov"}
              title={"Федоров Александр"}
              position={"Фронтендер"}
              age={"20 лет"}
              description={"бла-бла-бла"}
            >
              <picture
                className="image-wrapper team-card__floating-image"
                style={{ bottom: "-10px", left: "99px" }}
              >
                <img src={react} alt="React" className="image-wrapper__image" />
              </picture>
              <picture
                className="image-wrapper team-card__floating-image"
                style={{ bottom: "144px", left: "343px" }}
              >
                <img
                  src={js}
                  alt="JavaScript"
                  className="image-wrapper__image"
                />
              </picture>
              <p
                className="team-card__floating-text"
                style={{ bottom: "144px", left: "0px" }}
              >
                WEB <br />
                Разработка
              </p>
            </TeamCard>
          </SwiperSlide>
          <SwiperSlide className="team__slide">
            <TeamCard
              avatar={savchenko}
              avatarAlt={"Константин Савченко"}
              title={"Савченко Константин"}
              position={"Бэкендер"}
              age={"19 лет"}
              description={"бла-бла-бла"}
            >
              <picture
                className="image-wrapper team-card__floating-image"
                style={{ bottom: "95px", right: "199px" }}
              >
                <img
                  src={fastApi}
                  alt="fastAPI"
                  className="image-wrapper__image"
                />
              </picture>
              <picture
                className="image-wrapper team-card__floating-image"
                style={{ bottom: "0px", right: "59px" }}
              >
                <img
                  src={postgre}
                  alt="Postgre"
                  className="image-wrapper__image"
                />
              </picture>
              <picture
                className="image-wrapper team-card__floating-image"
                style={{ bottom: "125px", right: "0px" }}
              >
                <img
                  src={python}
                  alt="Python"
                  className="image-wrapper__image"
                />
              </picture>
            </TeamCard>
          </SwiperSlide>

          <SwiperSlide className="team__slide">
            <TeamCard
              avatar={alekseev}
              avatarAlt={"Дмитрий Алексеев"}
              title={"Алексеев Дмитрий"}
              position={"ML-инженер"}
              age={"19 лет"}
              description={"бла-бла-бла"}
            >
              <picture
                className="image-wrapper team-card__floating-image"
                style={{ bottom: "128px", left: "270px" }}
              >
                <img
                  src={python}
                  alt="Python"
                  className="image-wrapper__image"
                />
              </picture>
              <picture
                className="image-wrapper team-card__floating-image"
                style={{ bottom: "0px", left: "129px" }}
              >
                <img src={gc} alt="Gc" className="image-wrapper__image" />
              </picture>
              <p
                className="team-card__floating-text"
                style={{ bottom: "144px", left: "0px" }}
              >
                ML <br />
                алгоритмы
              </p>
            </TeamCard>
          </SwiperSlide>
          <SwiperSlide className="team__slide">
            <TeamCard
              avatar={arefev}
              avatarAlt={"Арефев Александр"}
              title={"Арефев Александр"}
              position={"ML-инженер"}
              age={"19 лет"}
              description={"бла-бла-бла"}
            >
              <picture
                className="image-wrapper team-card__floating-image"
                style={{ bottom: "118px", right: "200px" }}
              >
                <img
                  src={python}
                  alt="Python"
                  className="image-wrapper__image"
                />
              </picture>
            </TeamCard>
          </SwiperSlide>
        </Swiper>
      </div>
    </section>
  );
}

export default TeamSlider;
