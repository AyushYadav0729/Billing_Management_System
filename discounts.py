#membership_levels - silver, gold , platinum

def get_discounted_price(membership_level, total_amount):
    discount ={}
    discount['silver'] = 0.10
    discount['gold'] = 0.15
    discount['platinum'] = 0.25
    discount_price = total_amount - (total_amount * discount[membership_level.lower()])

    if membership_level not in discount:
        return total_amount
    return discount_price