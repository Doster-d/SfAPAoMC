import { useQuery } from "@tanstack/react-query";
import { getGeneralInfo } from "../api/getGeneralInfo";


export function useGetGeneralInfo() {
    return useQuery({
        queryKey: ['general'],
        queryFn: async () => (await getGeneralInfo()),
    })
}