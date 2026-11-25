import streamlit as st
from models import TripRequest
from planner_manager import PlannerManager

st.set_page_config(page_title="Travel Itinerary Concierge", page_icon="✈️", layout="wide")
st.title("✈️ Travel Itinerary Planning Concierge")
st.caption("Manager-worker multi-agent system with shared trip memory and a mandatory budget gate.")

with st.sidebar:
    st.header("Your trip")
    origin = st.text_input("Starting location", "Amritsar")
    destination = st.text_input("Destination", "Jaipur")
    days = st.slider("Number of days", 1, 14, 3)
    travellers = st.number_input("Travellers", 1, 12, 2)
    budget = st.number_input("Total budget (₹)", min_value=1000, value=35000, step=1000)
    hotel_category = st.selectbox("Hotel preference", ["Budget", "Standard", "Premium"])
    interests = st.multiselect("Interests", ["history", "food", "culture", "nature", "photography", "shopping", "science", "relaxation"],
                               default=["history", "food", "culture"])
    generate = st.button("Generate itinerary", type="primary", use_container_width=True)

st.info("Academic demo uses illustrative sample prices, not live availability or bookable offers.")
if generate:
    try:
        request = TripRequest(origin=origin, destination=destination, days=days,
            travellers=int(travellers), budget=float(budget),
            hotel_category=hotel_category, interests=interests)
        with st.spinner("Planner Manager is coordinating specialist agents..."):
            result, log = PlannerManager().plan(request)

        st.subheader(f"{origin} → {destination}")
        a, b, c = st.columns(3)
        a.metric("Estimated total", f"₹{result.total_cost:,.0f}")
        b.metric("Budget remaining", f"₹{result.remaining_budget:,.0f}")
        c.metric("Travellers / days", f"{travellers} / {days}")

        left, right = st.columns(2)
        with left:
            st.markdown("**Flight Worker**")
            if result.flight:
                st.write(result.flight.name, f"— ₹{result.flight.cost:,.0f}")
                st.caption(result.flight.description)
            else:
                st.warning("No flight option fits the remaining budget.")
        with right:
            st.markdown("**Hotel Worker**")
            if result.hotel:
                st.write(result.hotel.name, f"— ₹{result.hotel.cost:,.0f}")
                st.caption(result.hotel.description)
            else:
                st.warning("No hotel option fits the remaining budget.")

        st.subheader("Day-by-day itinerary")
        for day in result.days:
            with st.expander(day.title, expanded=True):
                if day.activities:
                    for item in day.activities:
                        st.markdown(f"- **{item.name}** — ₹{item.cost:,.0f}")
                        st.caption(item.description)
                else:
                    st.write("No activity could be added within the remaining budget.")

        st.subheader("Budget report")
        st.write(f"Budget: ₹{budget:,.0f} | Committed: ₹{result.total_cost:,.0f} | Remaining: ₹{result.remaining_budget:,.0f}")
        if result.rejected_items:
            with st.expander(f"Budget Worker rejections ({len(result.rejected_items)})"):
                for item in result.rejected_items:
                    st.warning(item)
        with st.expander("Agent delegation log"):
            for line in log:
                st.write(line)
        st.success("All selected items passed the Budget Worker gate.")
    except Exception as exc:
        st.error(f"Could not generate itinerary: {exc}")
else:
    st.markdown("### How the agents collaborate")
    st.markdown("1. Planner Manager reads the request and delegates tasks.\n"
                "2. Flight Worker compares flight candidates.\n"
                "3. Hotel Worker compares stay options.\n"
                "4. Activity Worker proposes interest-matched activities.\n"
                "5. Budget Worker approves or rejects every addition.\n"
                "6. Shared TripState stores choices, spend and remaining budget.")
