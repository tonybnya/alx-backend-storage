-- Task: Create a trigger that decreases the quantity
-- of an item after adding a new order
-- Quantity in the table items can be negative.
CREATE trigger decrease_qty after insert
ON orders for each row update items
SET quantity = quantity - NEW.number
WHERE NEW.item_name = name;
