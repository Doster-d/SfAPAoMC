import { createHashRouter } from "react-router-dom";
import Layout from "../../pages/layout/Layout";
import Mainpage from "../../pages/mainpage/Mainpage";
import FileInfo from "../../pages/fileInfo/FileInfo";
import ErrorPage from "../../pages/errorPage/ErrorPage";


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
            }
        ]
    }
])