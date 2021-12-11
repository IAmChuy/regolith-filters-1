{
	"format_version": "1.16.0",
	"minecraft:entity": {
		"description": {
			"identifier": f"{namespace}:pig_{color}",
			"is_spawnable": true,
			"is_summonable": true,
			"is_experimental": false
		},
		"components": {
			"minecraft:type_family": {
				"family": [
					f"pig_{color}",
					"pig",
					"mob"
				]
			},
			"minecraft:breathable": {
				"total_supply": 15,
				"suffocate_time": 0
			},
			"minecraft:health": {
				"value": 10,
				"max": 10
			},
			"minecraft:hurt_on_condition": {
				"damage_conditions": [
					{
						"filters": {
							"test": "in_lava",
							"subject": "self",
							"operator": "==",
							"value": true
						},
						"cause": "lava",
						"damage_per_tick": 4
					}
				]
			},
			"minecraft:movement": {
				"value": 0.25
			},
			"minecraft:navigation.walk": {
				"can_path_over_water": true,
				"avoid_water": true,
				"avoid_damage_blocks": true
			},
			"minecraft:movement.basic": {},
			"minecraft:jump.static": {},
			"minecraft:can_climb": {},
			"minecraft:collision_box": {
				"width": 0.9,
				"height": 0.9
			},
			"minecraft:despawn": {
				"despawn_from_distance": {}
			},
			"minecraft:behavior.float": {
				"priority": 2
			},
			"minecraft:behavior.panic": {
				"priority": 3,
				"speed_multiplier": 1.25
			},
			"minecraft:behavior.random_stroll": {
				"priority": 7,
				"speed_multiplier": 1.0
			},
			"minecraft:behavior.look_at_player": {
				"priority": 8,
				"look_distance": 6.0,
				"probability": 0.02
			},
			"minecraft:behavior.random_look_around": {
				"priority": 9
			},
			"minecraft:physics": {},
			"minecraft:pushable": {
				"is_pushable": true,
				"is_pushable_by_piston": true
			},
			"minecraft:conditional_bandwidth_optimization": {}
		}
	}
}