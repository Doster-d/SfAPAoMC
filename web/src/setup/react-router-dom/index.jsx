import { createHashRouter } from "react-router-dom";
import Layout from "../../pages/layout/Layout";
import Mainpage from "../../pages/mainpage/Mainpage";
import FileInfo from "../../pages/fileInfo/FileInfo";
import ErrorPage from "../../pages/errorPage/ErrorPage";
import SignIn, { loader as signInLoader } from "../../pages/signIn/SignIn";
import SignUp, { loader as signUpLoader } from "../../pages/signup/SignUp";
import Profile from "../../pages/profile/Profile";


export const router = createHashRouter([
    {
        path: '/',
        element: <Layout />,
        errorElement: <ErrorPage/>,
        children:[
            {
                index: true,
                element: <Mainpage />
            },
            {
                path: '/file/:fileId',
                element: <FileInfo/>
            },
            {
                path: '/signin',
                //loader: signInLoader,
                element: <SignIn/>
            },
            {
                path: '/signup',
                //loader: signUpLoader,
                element: <SignUp />
            },
            {
                path: '/profile',
                element: <Profile />
            }
        ]
    }
])