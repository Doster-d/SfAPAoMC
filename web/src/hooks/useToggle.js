import { useCallback, useState } from "react";

export function useToggle(init = false) {
    const [value, setValue] = useState(init);
    const toggle = useCallback(() => {
        setValue(prev => !prev)
      }, [])
    return [value, toggle];
}
