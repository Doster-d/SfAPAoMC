import { createHashRouter } from "react-router-dom";
import Layout from "../../pages/layout/Layout";
import Mainpage from "../../pages/mainpage/Mainpage";
import FileInfo from "../../pages/fileInfo/FileInfo";


export const router = createHashRouter([
    {
        path: '/',
        element: <Layout />,
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