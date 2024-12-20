import { createContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
    const [authTokens, setAuthTokens] = useState(() =>
        localStorage.getItem("authTokens") ? JSON.parse(localStorage.getItem("authTokens")) : null
    );

    const [user, setUser] = useState(() =>
        localStorage.getItem("authTokens") ? jwtDecode(localStorage.getItem("authTokens")) : null
    );

    const [loading, setLoading] = useState(true);

    const history = useNavigate();

    const loginUser = async (email, password) => {
        const response = await fetch("http://127.0.0.1:8000/api/token/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email, password
            })
        });
        const data = await response.json();
        console.log(data);
        if (response.status === 200) {
            setAuthTokens(data);
            setUser(jwtDecode(data.access));
            localStorage.setItem("authTokens", JSON.stringify(data));
            history("/");
        } else {
            alert("Неправильная почта или пароль");
        }
    }

    const registerUser = async (email, username, birthday, password, password_repeat) => {
        const response = await fetch("http://127.0.0.1:8000/api/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email, username, birthday, password, password_repeat
            })
        });
        if (response.status === 201) {
            history("/login");
        } else {
            console.log(response.status);
        }
    }

    const logoutUser = async () => {
        setAuthTokens(null);
        setUser("null");
        localStorage.removeItem("authTokens");
        history("/login");
    }

    const ContextData = {
        user,
        setUser,
        setAuthTokens,
        loginUser,
        registerUser,
        logoutUser
    }

    useEffect(() => {
        if (authTokens) {
            setUser(jwtDecode(authTokens.access));
        }
        setLoading(false);
    }, [authTokens, loading]);

    return (
        <AuthContext.Provider value={ContextData}>
          {loading ? <div>Загрузка...</div> : children}
        </AuthContext.Provider>
    );

};
