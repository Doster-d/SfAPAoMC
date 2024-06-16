function TeamCard({avatar, avatarAlt, title, age, position, description, children}) {
  return (
    <article className="team__card team-card">
      <picture className="image-wrapper team__image">
        <img
          src={avatar}
          alt={avatarAlt}
          className="image-wrapper__image team__image-bg"
        />
        <img
          src={avatar}
          alt={avatarAlt}
          className="image-wrapper__image"
        />
      </picture>
      <div className="team-card__info ">
        <h3 className="team-card__title">{title}</h3>
        <div className="team-card__addition">
          <p className="team-card__text">{position}</p>
          <p className="team-card__text">{age}</p>
        </div>
        <p className="team-card__text">
          {description}
        </p>
      </div>
      {children}
    </article>
  );
}

export default TeamCard;
