CREATE VIEW `new_view` AS
SELECT ehp.employe_id, e.id, ehp.position_id, p.id, e.first_name, e.last_name, p.title 
FROM employe_has_position ehp 
LEFT JOIN employe e ON ehp.employe_id = e.id 
LEFT JOIN `position` p on ehp.position_id = p.id 
ORDER BY ehp.employe_id 
