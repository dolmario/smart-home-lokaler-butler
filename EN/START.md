# Understand a local smart-home butler: an offline exercise

The original author's house butler called Hermes is a Python project on an ODROID H4, distinct from the Nous Hermes AI agent. This download is an own synthetic exercise, not the private operational house application. Existing Python3.10+ is sufficient; no extra libraries, installation, network, model or device calls.

1. Unzip into a new folder and read BUTLER-UEBUNG.py and DATEN-SYNTHETISCH.json.
2. Run: `python ./BUTLER-UEBUNG.py --data ./DATEN-SYNTHETISCH.json --state ./state.sqlite --output ./run-1`.
3. Open run-1/DASHBOARD.html. BERICHT.json retains the same results. The clock is deliberately fixed at2026-10-07T07:00:00UTC. Freshness requires age0..900seconds. Solar350W, battery58percent and two supplied dew points are fresh; the previous evening's heating reading is stale. Power in watts is not energy in kilowatt-hours.
4. Dew points inside12°C and outside8°C give only a moisture comparison. This is not an automatic ventilation recommendation: pollutants, weather, indoor temperature and building conditions remain unassessed. Missing/stale/wrong units produce unknown.
5. The switch request is off, with no acknowledgement and an observed on. The result is not_confirmed. A language model must not turn that into a claim of success.
6. Copy the input under a new filename. Set switch_ack to `{"request_id":"exercise-001","applied":true,"at":"2026-10-07T06:59:10+00:00"}` and switch_observation.state to off. Run again into a new output folder. synthetic_confirmation_matches only means the synthetic contract passes; no hardware is controlled.
7. Run the original input again with the same state.sqlite and a new --output ./run-2. First preparation was true; repeated preparation is false; stored_event_count stays1 after closing and reopening SQLite. The persistent unique day/event key deduplicates local preparation, not confirmed delivery. The status is prepared_simulation_not_sent.
8. Telegram incoming-update offsets and deduplication of outgoing scheduled briefings are separate concerns. A crash between sending and saving creates uncertain delivery. This kit neither sends nor proposes automatic blind resending.
9. Real vendor/calendar/device adapters, authentic acknowledgements, authorization and delivery handling require separate tests. Local orchestration does not make Telegram, vendor clouds, news or optional external AI offline. No private house data, addresses or credentials are provided.
10. Use the empty PRUEFPROTOKOLL.csv to record any future real tests. First map source→units/time→database→dashboard; place actions on a separate request→tool response→readback path. Heating control, energy savings and new device support are not freshly tested here.

Success in this exercise means understanding units/freshness, recognising an unconfirmed action and keeping exactly one prepared synthetic daily event across process restarts. It is not proof of a delivered message or operating hardware.
