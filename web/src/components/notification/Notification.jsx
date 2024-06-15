import { useEffect } from "react";
import './style.scss'
const Notification = ({ message, duration, onClose, type }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  return (
    <div style={{animationDuration: `${duration}ms`}} className={type === 'good' ? 'notification' : 'notification notification--bad'}>
      {message}
    </div>
  );
};

const NotificationContainer = ({ notifications, onClose }) => {
  return (
    <div className="notification-container">
      {notifications?.map((notification) => (
        <Notification
          key={notification.id}
          message={notification.message}
          duration={notification.duration}
          type={notification.type}
          onClose={() => onClose(notification.id)}
        />
      ))}
    </div>
  );
};

export default NotificationContainer;