import Layout from "@/components/Layout";
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'

const events = [
  { title: '出勤', start: new Date() }
]

export default function Monthly() {
  return (
    <Layout>
    <div>
      <h1>Monthly</h1>
      <FullCalendar
        plugins={[dayGridPlugin]}
        initialView='dayGridMonth'
        weekends={false}
        events={events}
        eventContent={renderEventContent}
      />
    </div>
    </Layout>
  )
}

function renderEventContent(eventInfo) {
  return (
    <>
      <b>{eventInfo.timeText}</b>
      <i>{eventInfo.event.title}</i>
    </>
  )
}