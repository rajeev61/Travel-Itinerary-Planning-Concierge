class BudgetWorker:
    name = "Budget Worker"
    def approve_and_add(self, item, state):
        # Mandatory gate: reject before shared state is mutated.
        if item.cost <= state.remaining:
            state.commit(item)
            return True, f"APPROVED: {item.name} (₹{item.cost:,.0f}); remaining ₹{state.remaining:,.0f}"
        message = f"REJECTED: {item.name} costs ₹{item.cost:,.0f}; only ₹{state.remaining:,.0f} remains."
        state.rejected_items.append(message)
        return False, message
