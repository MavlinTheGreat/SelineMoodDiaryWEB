import React, { useState, useEffect } from 'react';
import useAxios from "../../utils/useAxios";
import { jwtDecode } from "jwt-decode";

function About() {
  const [username, setUsername] = useState("");
  const api = useAxios();

  // интересный баг - если очистить базу данных на стороне бэкенда, то авторизация сохраняется)))
  useEffect(() => {
    const token = localStorage.getItem("authTokens");
    if (token) {
      const parsedTokens = JSON.parse(token); // Парсим токен из строки в объект
      const decoded = jwtDecode(parsedTokens.access); // Расшифровываем access-токен
      setUsername(decoded.username); // Сохраняем имя пользователя в state
    }
  }, []);

  return (
    <div>
      <h1>Привет, {username || "гость"}!</h1>
    </div>
  );
}

export default About;