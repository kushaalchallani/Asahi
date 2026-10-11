import { useCallback, useEffect, useState } from "react"
import { getCheckIn } from "../services/api"
import type { CheckIn as CheckInData } from "../types/checkIn"

export function useCheckIns(onCheckInCreated?: () => Promise<void>) {
  const [checkIns, setCheckIns] = useState<CheckInData[]>([])

  useEffect(() => {
    async function loadCheckIns() {
      try {
        const data = await getCheckIn()
        setCheckIns(data)
      } catch (error) {
        console.error("Failed to load check-ins:", error)
      }
    }

    void loadCheckIns()
  }, [])

  const handleCheckInCreated = useCallback(
    async (newCheckIn: CheckInData) => {
      setCheckIns((currentCheckIns) => {
        if (currentCheckIns.some((checkIn) => checkIn.id === newCheckIn.id)) {
          return currentCheckIns
        }

        return [newCheckIn, ...currentCheckIns].sort(
          (a, b) =>
            new Date(b.created_at).getTime() -
            new Date(a.created_at).getTime()
        )
      })

      if (onCheckInCreated) {
        await onCheckInCreated()
      }
    },
    [onCheckInCreated]
  )

  return { checkIns, handleCheckInCreated }
}
