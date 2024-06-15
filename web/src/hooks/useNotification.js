import { useState, useCallback } from 'react';

const useNotifications = () => {
    const [notifications, setNotifications] = useState([]);
  
    const addNotification = useCallback((message, type, duration = 3000) => {
      const id = Date.now();
      setNotifications((prevNotifications) => [
        ...prevNotifications,
        { id, message, duration, type }
      ]);
  
      setTimeout(() => {
        setNotifications((prevNotifications) =>
          prevNotifications.filter((notification) => notification.id !== id)
        );
      }, duration);
    }, []);
  
    const removeNotification = useCallback((id) => {
      setNotifications((prevNotifications) =>
        prevNotifications.filter((notification) => notification.id !== id)
      );
    }, []);
  
    return {
      notifications,
      addNotification,
      removeNotification
    };
  };

export default useNotifications;