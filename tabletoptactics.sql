--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2 (Debian 15.2-2)
-- Dumped by pg_dump version 15.2 (Debian 15.2-2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tablefunc; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS tablefunc WITH SCHEMA public;


--
-- Name: EXTENSION tablefunc; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION tablefunc IS 'functions that manipulate whole tables, including crosstab';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: armies; Type: TABLE; Schema: public; Owner: philip
--

CREATE TABLE public.armies (
    id integer NOT NULL,
    show_id integer NOT NULL,
    player_id integer NOT NULL,
    faction_id integer NOT NULL,
    subfaction_id integer,
    winner boolean
);


ALTER TABLE public.armies OWNER TO philip;

--
-- Name: armies_id_seq; Type: SEQUENCE; Schema: public; Owner: philip
--

CREATE SEQUENCE public.armies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.armies_id_seq OWNER TO philip;

--
-- Name: armies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: philip
--

ALTER SEQUENCE public.armies_id_seq OWNED BY public.armies.id;


--
-- Name: campaigns; Type: TABLE; Schema: public; Owner: philip
--

CREATE TABLE public.campaigns (
    id integer NOT NULL,
    campaign text NOT NULL
);


ALTER TABLE public.campaigns OWNER TO philip;

--
-- Name: campaigns_id_seq; Type: SEQUENCE; Schema: public; Owner: philip
--

CREATE SEQUENCE public.campaigns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaigns_id_seq OWNER TO philip;

--
-- Name: campaigns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: philip
--

ALTER SEQUENCE public.campaigns_id_seq OWNED BY public.campaigns.id;


--
-- Name: factions; Type: TABLE; Schema: public; Owner: philip
--

CREATE TABLE public.factions (
    id integer NOT NULL,
    faction text NOT NULL,
    game_id integer NOT NULL
);


ALTER TABLE public.factions OWNER TO philip;

--
-- Name: factions_id_seq; Type: SEQUENCE; Schema: public; Owner: philip
--

CREATE SEQUENCE public.factions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.factions_id_seq OWNER TO philip;

--
-- Name: factions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: philip
--

ALTER SEQUENCE public.factions_id_seq OWNED BY public.factions.id;


--
-- Name: games; Type: TABLE; Schema: public; Owner: philip
--

CREATE TABLE public.games (
    id integer NOT NULL,
    game text NOT NULL
);


ALTER TABLE public.games OWNER TO philip;

--
-- Name: games_id_seq; Type: SEQUENCE; Schema: public; Owner: philip
--

CREATE SEQUENCE public.games_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.games_id_seq OWNER TO philip;

--
-- Name: games_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: philip
--

ALTER SEQUENCE public.games_id_seq OWNED BY public.games.id;


--
-- Name: leagueseasons; Type: TABLE; Schema: public; Owner: philip
--

CREATE TABLE public.leagueseasons (
    id integer NOT NULL,
    show_id integer NOT NULL,
    league_season integer NOT NULL,
    episode integer NOT NULL
);


ALTER TABLE public.leagueseasons OWNER TO philip;

--
-- Name: leagueseasons_id_seq; Type: SEQUENCE; Schema: public; Owner: philip
--

CREATE SEQUENCE public.leagueseasons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.leagueseasons_id_seq OWNER TO philip;

--
-- Name: leagueseasons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: philip
--

ALTER SEQUENCE public.leagueseasons_id_seq OWNED BY public.leagueseasons.id;


--
-- Name: narrativeshows; Type: TABLE; Schema: public; Owner: philip
--

CREATE TABLE public.narrativeshows (
    id integer NOT NULL,
    show_id integer NOT NULL,
    campaign_id integer NOT NULL,
    campaign_sequence integer NOT NULL
);


ALTER TABLE public.narrativeshows OWNER TO philip;

--
-- Name: narrativeshows_id_seq; Type: SEQUENCE; Schema: public; Owner: philip
--

CREATE SEQUENCE public.narrativeshows_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.narrativeshows_id_seq OWNER TO philip;

--
-- Name: narrativeshows_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: philip
--

ALTER SEQUENCE public.narrativeshows_id_seq OWNED BY public.narrativeshows.id;


--
-- Name: players; Type: TABLE; Schema: public; Owner: philip
--

CREATE TABLE public.players (
    id integer NOT NULL,
    fullname text NOT NULL,
    nickname text NOT NULL
);


ALTER TABLE public.players OWNER TO philip;

--
-- Name: players_id_seq; Type: SEQUENCE; Schema: public; Owner: philip
--

CREATE SEQUENCE public.players_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.players_id_seq OWNER TO philip;

--
-- Name: players_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: philip
--

ALTER SEQUENCE public.players_id_seq OWNED BY public.players.id;


--
-- Name: shows; Type: TABLE; Schema: public; Owner: philip
--

CREATE TABLE public.shows (
    id integer NOT NULL,
    release_date date NOT NULL,
    game_id integer NOT NULL,
    showtype_id integer NOT NULL,
    slug text NOT NULL,
    youtube_slug text,
    servoskull_id integer
);


ALTER TABLE public.shows OWNER TO philip;

--
-- Name: shows_id_seq; Type: SEQUENCE; Schema: public; Owner: philip
--

CREATE SEQUENCE public.shows_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shows_id_seq OWNER TO philip;

--
-- Name: shows_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: philip
--

ALTER SEQUENCE public.shows_id_seq OWNED BY public.shows.id;


--
-- Name: showtypes; Type: TABLE; Schema: public; Owner: philip
--

CREATE TABLE public.showtypes (
    id integer NOT NULL,
    showtype text NOT NULL
);


ALTER TABLE public.showtypes OWNER TO philip;

--
-- Name: showtypes_id_seq; Type: SEQUENCE; Schema: public; Owner: philip
--

CREATE SEQUENCE public.showtypes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.showtypes_id_seq OWNER TO philip;

--
-- Name: showtypes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: philip
--

ALTER SEQUENCE public.showtypes_id_seq OWNED BY public.showtypes.id;


--
-- Name: subfactions; Type: TABLE; Schema: public; Owner: philip
--

CREATE TABLE public.subfactions (
    id integer NOT NULL,
    subfaction text NOT NULL,
    faction_id integer NOT NULL
);


ALTER TABLE public.subfactions OWNER TO philip;

--
-- Name: subfactions_id_seq; Type: SEQUENCE; Schema: public; Owner: philip
--

CREATE SEQUENCE public.subfactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subfactions_id_seq OWNER TO philip;

--
-- Name: subfactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: philip
--

ALTER SEQUENCE public.subfactions_id_seq OWNED BY public.subfactions.id;


--
-- Name: armies id; Type: DEFAULT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.armies ALTER COLUMN id SET DEFAULT nextval('public.armies_id_seq'::regclass);


--
-- Name: campaigns id; Type: DEFAULT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.campaigns ALTER COLUMN id SET DEFAULT nextval('public.campaigns_id_seq'::regclass);


--
-- Name: factions id; Type: DEFAULT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.factions ALTER COLUMN id SET DEFAULT nextval('public.factions_id_seq'::regclass);


--
-- Name: games id; Type: DEFAULT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.games ALTER COLUMN id SET DEFAULT nextval('public.games_id_seq'::regclass);


--
-- Name: leagueseasons id; Type: DEFAULT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.leagueseasons ALTER COLUMN id SET DEFAULT nextval('public.leagueseasons_id_seq'::regclass);


--
-- Name: narrativeshows id; Type: DEFAULT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.narrativeshows ALTER COLUMN id SET DEFAULT nextval('public.narrativeshows_id_seq'::regclass);


--
-- Name: players id; Type: DEFAULT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.players ALTER COLUMN id SET DEFAULT nextval('public.players_id_seq'::regclass);


--
-- Name: shows id; Type: DEFAULT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.shows ALTER COLUMN id SET DEFAULT nextval('public.shows_id_seq'::regclass);


--
-- Name: showtypes id; Type: DEFAULT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.showtypes ALTER COLUMN id SET DEFAULT nextval('public.showtypes_id_seq'::regclass);


--
-- Name: subfactions id; Type: DEFAULT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.subfactions ALTER COLUMN id SET DEFAULT nextval('public.subfactions_id_seq'::regclass);


--
-- Data for Name: armies; Type: TABLE DATA; Schema: public; Owner: philip
--

COPY public.armies (id, show_id, player_id, faction_id, subfaction_id, winner) FROM stdin;
8	4	6	7	5	\N
17	9	5	14	\N	\N
24	15	1	18	14	\N
42	25	4	4	4	\N
53	31	3	3	3	\N
66	38	1	28	\N	\N
67	38	5	21	\N	\N
35	21	2	25	34	\N
110	60	6	15	40	\N
111	60	2	2	\N	\N
153	81	5	18	14	f
155	82	3	19	65	t
154	82	4	22	64	f
138	74	3	3	3	f
102	56	6	7	5	t
103	56	9	1	51	f
74	42	7	20	16	t
75	42	1	27	31	f
47	28	1	18	14	t
48	28	2	25	34	f
31	19	6	23	\N	t
32	19	4	24	19	f
1	1	1	1	1	f
3	2	3	3	3	t
4	2	4	4	4	f
6	3	5	1	1	t
7	3	6	6	\N	t
5	3	1	5	\N	f
9	5	6	9	6	t
10	5	3	8	7	f
12	6	6	11	9	t
14	7	1	13	\N	t
13	7	5	12	\N	f
15	8	6	1	10	t
16	8	1	11	\N	f
18	10	2	2	11	t
19	10	4	15	12	f
21	11	1	11	\N	t
22	14	5	1	13	t
23	14	4	16	\N	f
25	16	6	9	6	t
26	16	1	19	15	f
28	17	1	14	\N	t
29	18	3	21	17	t
30	18	4	22	18	f
34	20	5	1	20	t
33	20	2	7	21	f
39	23	6	11	9	t
36	22	6	11	9	t
37	22	5	26	\N	f
38	23	3	1	22	f
41	24	5	1	1	t
40	24	1	27	23	f
44	26	1	28	25	f
46	27	3	18	14	t
45	27	2	2	26	f
49	29	6	23	24	t
50	29	5	29	27	f
52	30	4	15	12	t
51	30	6	27	28	f
55	32	5	1	29	t
54	32	1	27	30	f
57	33	5	1	1	t
56	33	1	27	31	f
58	34	6	4	4	t
60	35	6	7	\N	t
61	35	3	18	14	f
63	36	6	23	33	t
62	36	3	24	32	f
65	37	1	30	35	t
64	37	2	25	34	f
68	39	5	6	36	t
69	39	4	31	37	f
71	40	4	32	38	f
72	41	6	1	39	t
73	41	1	33	\N	f
76	43	1	33	\N	t
77	43	6	15	40	f
79	44	3	28	25	t
78	44	8	34	41	f
81	45	5	26	43	t
82	46	6	9	6	t
83	46	1	19	44	f
85	47	2	25	34	t
84	47	4	32	45	f
86	48	3	4	46	t
87	48	4	16	47	f
88	49	3	16	48	t
89	49	6	1	10	f
156	84	1	7	5	f
157	84	3	7	5	f
158	84	5	14	\N	t
160	84	6	26	56	t
99	54	5	29	27	t
98	54	4	22	49	f
100	55	1	5	\N	f
105	57	5	1	1	f
106	58	7	20	16	f
104	57	1	27	30	t
107	58	1	27	30	t
108	59	4	24	32	t
112	61	3	12	53	t
113	61	1	23	33	f
114	62	5	6	36	f
115	62	4	32	54	t
117	63	5	14	\N	f
116	63	1	18	55	t
119	64	1	7	5	t
118	64	3	26	56	f
120	65	6	1	10	t
121	65	7	20	16	f
123	66	3	8	7	t
124	67	1	27	31	t
125	67	10	36	58	f
127	68	6	9	6	t
126	68	4	24	32	f
129	69	3	16	48	t
128	69	1	27	30	f
131	70	2	2	\N	t
130	70	1	33	59	f
133	71	3	16	48	f
97	53	3	7	5	f
96	53	5	14	\N	t
135	72	3	21	60	t
134	72	4	24	19	f
136	73	5	14	\N	f
137	73	3	20	61	t
140	75	1	14	\N	t
141	75	4	32	38	f
142	76	6	1	10	t
144	77	6	9	62	t
145	77	5	29	27	f
147	78	2	25	34	f
146	78	6	27	28	t
148	79	3	13	63	f
149	79	1	19	15	t
150	80	6	1	10	t
151	80	5	6	36	f
95	52	5	1	13	f
161	85	1	27	30	f
219	114	7	20	16	\N
222	116	4	32	54	\N
237	124	5	6	36	\N
238	125	1	27	30	\N
243	128	3	16	48	\N
244	129	6	1	10	\N
267	141	6	1	10	\N
268	141	3	16	47	\N
290	152	5	1	1	t
289	152	4	15	12	f
291	153	6	27	28	t
292	153	1	27	30	f
152	81	3	5	\N	t
286	150	3	38	98	t
285	150	2	2	26	f
274	144	5	1	95	t
273	144	1	27	30	f
271	143	1	18	14	t
272	143	4	4	4	f
261	138	3	12	53	t
262	138	16	34	41	f
259	137	7	20	16	t
260	137	3	36	92	f
235	123	5	14	\N	t
236	123	1	18	14	f
221	115	5	1	22	f
220	115	4	16	77	t
198	103	1	37	71	t
197	103	5	21	60	f
294	154	5	1	94	f
293	154	2	26	70	t
139	74	2	25	34	t
2	1	2	2	2	t
11	6	2	7	8	f
20	11	5	1	1	f
27	17	7	20	16	f
43	26	6	23	24	t
295	155	4	4	4	f
296	155	2	25	34	t
59	34	5	14	\N	f
70	40	5	1	1	t
80	45	4	4	42	f
297	156	3	9	62	t
298	156	4	24	100	f
159	84	6	1	13	t
299	157	5	11	9	t
300	157	2	5	\N	f
101	55	3	31	50	t
109	59	3	35	52	f
122	66	1	23	57	f
132	71	7	20	16	t
143	76	4	32	54	f
301	158	1	28	25	t
302	158	5	29	27	f
164	86	6	9	6	t
165	87	1	1	13	t
167	88	3	8	7	t
168	88	4	22	49	f
169	89	5	6	36	f
170	89	7	20	16	t
191	100	2	7	68	t
192	100	5	14	\N	f
171	90	6	1	10	t
172	90	7	20	16	f
194	101	5	12	\N	f
195	102	4	15	69	f
196	102	2	26	70	t
209	109	5	12	53	f
210	109	1	19	73	t
174	91	3	16	48	t
173	91	1	27	30	f
200	104	9	1	51	f
199	104	1	5	\N	t
176	92	7	20	16	f
202	105	4	22	18	f
201	105	3	24	72	t
203	106	1	5	\N	f
204	106	2	7	5	t
205	107	3	8	7	f
206	107	5	12	53	t
207	108	1	19	73	f
208	108	3	21	17	t
178	93	3	16	48	t
211	110	6	4	42	f
212	110	11	27	30	t
213	111	5	7	5	f
214	111	1	18	74	t
179	94	5	6	36	t
180	94	4	32	54	f
215	112	6	15	75	t
216	112	12	15	\N	f
218	113	2	14	\N	f
217	113	4	31	76	t
182	95	7	20	16	t
224	117	5	20	61	f
223	117	2	25	78	t
183	96	5	6	36	f
184	96	3	16	48	t
225	118	13	1	1	t
226	118	6	27	28	f
227	119	2	2	26	t
228	119	1	5	\N	f
230	120	1	5	\N	f
185	97	6	1	10	t
186	97	1	27	30	f
231	121	5	20	61	t
232	121	4	32	80	f
233	122	3	7	21	t
234	122	14	36	81	f
187	98	5	6	36	f
188	98	1	27	30	t
240	126	15	4	4	f
190	99	6	1	10	t
189	99	3	16	48	f
241	127	3	1	83	t
242	127	2	25	34	f
246	130	5	7	5	t
245	130	4	31	84	f
247	131	3	3	3	t
248	131	15	4	4	f
249	132	1	1	1	t
250	132	3	27	85	f
252	133	5	6	87	f
254	134	1	2	88	f
253	134	4	4	\N	t
256	135	5	6	90	f
255	135	3	38	89	t
258	136	5	20	91	t
257	136	4	31	50	f
263	139	5	26	93	f
264	139	3	30	35	t
265	140	5	1	94	f
266	140	3	7	68	t
276	145	5	20	16	t
277	146	2	25	97	t
278	146	4	32	54	f
280	147	5	14	\N	f
279	147	3	16	47	t
284	149	1	1	22	t
283	149	3	36	81	f
288	151	1	11	\N	t
287	151	2	25	99	f
282	148	1	1	22	f
269	142	6	1	10	t
270	142	3	16	47	f
94	52	1	7	5	t
162	85	4	32	54	t
163	86	3	21	66	f
166	87	4	16	67	f
93	51	3	7	5	t
92	51	1	14	\N	f
193	101	3	35	52	t
90	50	1	7	5	t
91	50	5	14	\N	f
175	92	1	27	30	t
177	93	4	32	54	f
181	95	4	32	54	f
229	120	5	6	79	t
239	126	4	32	82	t
251	133	1	33	86	t
303	159	5	14	\N	t
304	159	4	4	4	f
275	145	1	27	96	f
281	148	3	36	81	t
305	160	1	27	30	t
306	160	4	1	95	f
307	161	6	27	28	t
308	161	3	36	81	f
309	162	1	27	31	t
310	162	5	1	22	f
311	163	5	6	101	f
312	163	6	15	40	t
313	164	4	32	54	f
314	164	3	14	\N	t
315	165	3	14	\N	t
316	165	4	32	54	f
317	166	2	2	26	f
318	166	3	16	47	t
319	167	4	15	\N	f
320	167	6	4	102	t
321	168	5	1	1	t
322	168	3	11	9	f
323	169	4	1	39	t
324	169	5	26	93	f
325	170	1	31	84	f
326	170	6	4	4	t
327	171	5	1	95	t
328	171	1	7	5	f
329	172	3	30	35	t
330	172	4	4	103	f
331	173	1	1	39	t
332	173	3	3	104	f
333	174	1	1	39	t
334	174	3	3	104	f
335	175	5	14	\N	f
336	175	3	31	50	t
337	176	17	18	74	f
338	176	6	15	105	t
339	177	1	33	\N	t
340	177	5	14	\N	f
341	178	1	1	13	f
342	178	3	16	47	t
343	179	1	33	59	t
344	179	2	25	97	f
345	180	3	32	106	f
346	180	4	31	50	t
347	181	4	32	54	t
348	181	2	25	97	f
349	182	17	1	22	t
350	182	5	20	91	f
351	183	4	32	45	t
352	183	5	6	79	f
353	184	5	14	\N	f
354	184	6	7	5	t
355	185	1	27	30	f
356	185	6	15	\N	t
357	186	6	1	10	t
358	186	5	20	16	f
359	187	3	30	35	t
360	187	5	20	91	f
361	188	3	2	2	t
362	188	5	26	107	f
363	189	3	30	108	f
364	189	2	25	97	t
365	190	3	7	5	f
366	190	5	26	93	t
367	191	3	30	35	t
368	191	1	1	1	f
369	192	4	22	18	t
370	192	5	21	17	f
371	193	1	33	86	t
372	193	6	27	28	f
373	194	1	4	42	t
374	194	5	1	1	f
375	195	4	32	38	f
376	195	17	1	22	t
377	196	1	33	59	f
378	196	9	1	51	t
379	197	3	3	3	f
380	197	1	18	14	t
381	198	3	3	104	t
382	198	5	1	94	f
383	199	4	4	103	f
384	199	5	6	101	t
385	200	2	25	34	f
386	200	6	7	5	t
387	201	3	8	7	t
388	201	4	24	19	f
389	202	4	4	4	f
390	202	6	7	5	t
\.


--
-- Data for Name: campaigns; Type: TABLE DATA; Schema: public; Owner: philip
--

COPY public.campaigns (id, campaign) FROM stdin;
1	Cinder Ark
2	Waaagh! Skulldagga
3	Gulkis Prime
4	Gerunda Hive
5	Dharros Prime
6	Tahnus IX
\.


--
-- Data for Name: factions; Type: TABLE DATA; Schema: public; Owner: philip
--

COPY public.factions (id, faction, game_id) FROM stdin;
1	Space Marines	1
2	Adeptus Custodes	1
3	Thousand Sons	1
4	Aeldari	1
5	Chaos Daemons	1
6	Grey Knights	1
7	Orks	1
8	Seraphon	2
9	Soulblight Gravelords	2
11	World Eaters	1
12	Maggotkin of Nurgle	2
13	Ogor Mawtribes	2
14	Astra Militarum	1
15	Drukhari	1
16	Necrons	1
18	Leagues of Votann	1
19	Slaves to Darkness	2
20	T'au Empire	1
21	Stormcast Eternals	2
22	Hedonites of Slaanesh	2
23	Idoneth Deepkin	2
24	Ossiarch Bonereapers	2
25	Adeptus Mechanicus	1
26	Imperial Knights	1
27	Chaos Space Marines	1
28	Nighthaunt	2
29	Orruk Warclans	2
30	Chaos Knights	1
31	Adepta Sororitas	1
32	Tyranids	1
33	Death Guard	1
34	Sylvaneth	2
35	Blades of Khorne	2
36	Genestealer Cults	1
37	Skaven	2
38	Harlequins	1
\.


--
-- Data for Name: games; Type: TABLE DATA; Schema: public; Owner: philip
--

COPY public.games (id, game) FROM stdin;
1	Warhammer 40,000
2	Age of Sigmar
\.


--
-- Data for Name: leagueseasons; Type: TABLE DATA; Schema: public; Owner: philip
--

COPY public.leagueseasons (id, show_id, league_season, episode) FROM stdin;
1	99	1	1
2	98	1	2
3	97	1	3
4	96	1	4
5	95	1	5
6	94	1	6
7	93	1	7
8	92	1	8
9	91	1	9
10	90	1	10
11	89	1	11
12	85	1	12
13	80	1	13
14	76	1	14
15	71	1	15
16	69	1	16
17	65	1	17
18	62	1	18
19	58	1	19
20	49	1	20
21	2	2	1
22	28	2	2
23	74	2	3
24	123	2	4
25	143	2	5
26	155	2	6
27	159	2	7
28	184	2	8
29	197	2	9
30	200	2	10
31	202	2	11
\.


--
-- Data for Name: narrativeshows; Type: TABLE DATA; Schema: public; Owner: philip
--

COPY public.narrativeshows (id, show_id, campaign_id, campaign_sequence) FROM stdin;
1	3	1	4
2	11	1	3
3	24	1	2
4	33	1	1
5	50	2	1
6	51	2	2
7	52	2	3
8	53	2	4
9	64	2	5
10	84	2	6
11	142	3	1
12	141	3	2
13	148	4	1
14	149	4	2
15	164	5	1
16	165	5	2
17	173	6	1
18	174	6	2
\.


--
-- Data for Name: players; Type: TABLE DATA; Schema: public; Owner: philip
--

COPY public.players (id, fullname, nickname) FROM stdin;
1	Joe Ponting	Beard
2	Stig	Stig
3	Michael Hebditch	Chef
4	Katie Foad	Jinx
5	James Jordan	Bard
6	Lawrence Baker	Spider
7	Fletcher Giles	Fletch
8	Josh Hill	Warhipster
9	David Pettitt	Dave
10	Mark	Mark
11	David Ugolini	Gizmo
12	Ridvan Martinez	Blade
13	Maxine Blythin	Maxine
14	Ed Pemberton	Ed
15	Matt Jarvis	Matt
16	David Methven	Methven
17	Sam Weeks	Sam
\.


--
-- Data for Name: shows; Type: TABLE DATA; Schema: public; Owner: philip
--

COPY public.shows (id, release_date, game_id, showtype_id, slug, youtube_slug, servoskull_id) FROM stdin;
52	2022-11-01	1	3	deathwatch-vs-orks-s1-ep3-warhammer-40000-narrative-report	\N	4
50	2022-10-01	1	3	new-crusade-series-orks-vs-astra-militarum-warhammer-40000-narrative-report	Ftj_CXkclbQ	4
117	2022-09-06	1	1	tau-empire-vs-adeptus-mechanicus-warhammer-40000-battle-report	\N	6
15	2023-02-16	1	4	beards-leagues-of-votann-league-list-warhammer-40000-list-analysis	jcE_OgcP5RM	\N
21	2023-02-09	1	4	stigs-league-adeptus-mechanicus-warhammer-40000-list-analysis	M8FD9yoKhUY	\N
25	2023-02-02	1	4	jinxs-league-craftworlds-warhammer-40000-list-analysis	hm6__hG-M4g	\N
4	2023-03-02	1	4	spiders-orks-league-list-warhammer-40000-list-analysis	_gYSoQ8vGL8	\N
3	2023-03-03	1	3	imperium-vs-chaos-daemons-warhammer-40000-narrative-report-finale	\N	\N
9	2023-02-23	1	4	bards-astra-militarum-league-list-warhammer-40000-list-analysis	kKzyzHwvOBo	\N
82	2023-03-18	2	1	hedonites-of-slaanesh-vs-slaves-to-darkness-age-of-sigmar-battle-report	7UHibjkN0tk	5
74	2023-03-17	1	2	thousand-sons-vs-adeptus-mechanicus-season-2-ep-3-warhammer-40000-league-report	\N	4
56	2023-03-14	1	1	orks-vs-black-templars-warhammer-40000-battle-report	\N	3
42	2023-03-11	1	1	tau-empire-vs-chaos-space-marines-warhammer-40000-battle-report	wvX7H-Yxsdc	6
28	2023-03-10	1	2	leagues-of-votann-vs-adeptus-mechanicus-season-2-ep-2-warhammer-40000-league-report	\N	4
19	2023-03-08	2	1	ossiarch-bonereapers-vs-idoneth-deepkin-age-of-sigmar-battle-report-2	\N	3
1	2023-03-07	1	1	adeptus-custodes-vs-ravenwing-warhammer-40000-battle-report	\N	5
5	2023-03-01	2	1	seraphon-vs-soulblight-gravelords-age-of-sigmar-battle-report	\N	5
6	2023-02-28	1	1	orks-vs-world-eaters-warhammer-40000-battle-report	\N	1
7	2023-02-25	2	1	maggotkin-of-nurgle-vs-ogor-mawtribes-age-of-sigmar-battle-report	32P8JUnCDuk	3
8	2023-02-24	1	1	flesh-tearers-vs-world-eaters-boarding-action-battle-report	\N	5
10	2023-02-21	1	1	drukhari-vs-adeptus-custodes-warhammer-40000-battle-report-2	\N	5
11	2023-02-18	1	3	dark-angels-vs-world-eaters-warhammer-40000-narrative-report	U5kKRIX5Arg	6
14	2023-02-17	1	1	necrons-vs-deathwatch-boarding-action-battle-report	\N	1
16	2023-02-15	2	1	slaves-to-darkness-vs-soulblight-graveyards-age-of-sigmar-battle-report	\N	5
17	2023-02-14	1	1	astra-militarum-vs-tau-empire-warhammer-40000-battle-report	\N	5
18	2023-02-11	2	1	hedonites-of-slaanesh-vs-stormcast-eternals-age-of-sigmar-battle-report	rWQ0pDZLCWU	5
20	2023-02-10	1	1	orks-vs-crimson-fists-warhammer-40000-battle-report	\N	3
22	2023-02-07	1	1	new-codex-world-eaters-vs-imperial-knights-warhammer-40000-battle-report	\N	3
23	2023-02-04	1	1	new-codex-world-eaters-vs-ultramarines-warhammer-40000-battle-report	Ehp79tXRXak	4
24	2023-02-03	1	3	dark-angels-vs-red-corsairs-warhammer-40000-narrative-report	\N	4
26	2023-02-01	2	1	idoneth-deepkin-vs-nighthaunt-age-of-sigmar-battle-report	\N	5
27	2023-01-31	1	1	adeptus-custodes-vs-leagues-of-votann-warhammer-40000-battle-report	\N	5
29	2023-01-28	2	1	ironjawz-vs-idoneth-deepkin-age-of-sigmar-battle-report	cWoEJJHTVQ0	4
30	2023-01-27	1	1	emperors-children-vs-drukhari-warhammer-40000-boarding-action-battle-report	\N	1
32	2023-01-24	1	1	iron-warriors-vs-iron-hands-warhammer-40000-battle-report	\N	3
33	2023-01-21	1	3	dark-angels-vs-black-legion-warhammer-40000-narrative-report	kKkvlOBv20s	4
34	2023-01-20	1	1	ulthwe-vs-astra-militarum-warhammer-40000-battle-report	\N	4
35	2023-01-19	1	1	orks-vs-leagues-of-votann-boarding-action-battle-report	IpdMFb1uZS8	1
36	2023-01-18	2	1	ossiarch-bonereapers-vs-idoneth-deepkin-age-of-sigmar-battle-report	\N	5
38	2023-01-14	2	1	nighthaunt-vs-stormcast-eternals-age-of-sigmar-battle-report	IkUBMr_q_gE	3
39	2023-01-13	1	1	grey-knights-vs-adepta-sororitas-warhammer-40000-battle-report	\N	1
40	2023-01-10	1	1	dark-angels-vs-tyranids-warhammer-40000-boarding-action-battle-report	\N	1
41	2023-01-07	1	1	new-boarding-action-space-marines-vs-deathguard-warhammer-40000-boarding-action-battle-report	IuroVhK6gjc	3
43	2023-01-06	1	1	death-guard-vs-drukhari-warhammer-40000-battle-report	\N	5
44	2023-01-04	2	1	nighthaunt-vs-sylvaneth-age-of-sigmar-battle-report	\N	6
45	2023-01-03	1	1	craftworlds-vs-imperial-knights-warhammer-40000-battle-report	\N	1
46	2022-12-31	2	1	slaves-to-darkness-vs-soulblight-gravelords-age-of-sigmar-battle-report	ctuJyewDRDc	4
47	2022-12-30	1	1	tyranids-vs-adeptus-mechanicus-warhammer-40000-battle-report	\N	6
48	2022-12-27	1	1	craftworlds-vs-necrons-warhammer-40000-battle-report	\N	5
54	2022-12-21	2	1	ironjawz-vs-hedonites-of-slannesh-age-of-sigmar-battle-report	\N	3
55	2022-12-20	1	1	chaos-daemons-vs-adepta-sororitas-warhammer-40000-battle-report	\N	5
57	2022-12-17	1	1	dark-angels-vs-iron-warriors-warhammer-40000-battle-report	Am19qlTc4ac	6
58	2022-12-16	1	2	iron-warriors-vs-tau-empire-season-1-ep19-warhammer-40000-league-report	\N	4
59	2022-12-14	2	1	blades-of-khorne-vs-ossiarch-bonereapers-warhammer-age-of-sigmar-battle-report	\N	5
60	2022-12-13	1	1	drukhari-vs-adeptus-custodes-warhammer-40000-battle-report	\N	5
62	2022-12-09	1	2	grey-knights-vs-tyranids-season-1-ep18-warhammer-40000-league-report	\N	1
63	2022-12-06	1	1	leagues-of-votann-vs-astra-militarum-warhammer-40000-battle-report	\N	4
65	2022-12-02	1	2	flesh-tearers-vs-tau-empire-season-1-ep17-warhammer-40000-league-report	\N	4
66	2022-11-30	2	1	idoneth-deepkin-vs-seraphon-warhammer-age-of-sigmar-battle-report	\N	6
67	2022-11-29	1	1	black-legion-vs-genestealer-cults-warhammer-40000-battle-report	\N	6
69	2022-11-25	1	2	necrons-vs-iron-warriors-season-1-ep16-warhammer-40000-league-report	\N	5
70	2022-11-22	1	1	death-guard-vs-adeptus-custodes-warhammer-40000-battle-report	\N	4
53	2022-11-18	1	3	astra-militarum-vs-orks-warhammer-40000-narrative-report	\N	4
72	2022-11-16	2	1	ossiarch-bonereapers-vs-stormcast-eternals-age-of-sigmar-battle-report	\N	6
73	2022-11-15	1	1	new-codex-astra-militarum-vs-tau-empire-warhammer-40000-battle-report	\N	1
79	2022-11-05	2	1	new-battletomes-slaves-to-darkness-vs-ogor-mawtribes-age-of-sigmar-battle-report	qmXtLcQ5CnE	5
80	2022-11-04	1	2	flesh-tearers-vs-grey-knights-season-1-ep13-warhammer-40000-league-report	\N	1
85	2022-10-28	1	2	iron-warriors-vs-tyranids-season-1-ep12-warhammer-40000-league-report	\N	5
31	2023-01-26	1	4	chefs-league-thousand-sons-warhammer-40000-list-analysis	PD_w7GzTIBQ	\N
86	2022-10-26	2	1	soulblight-gravelords-vs-stormcast-eternals-age-of-sigmar-battle-report	\N	5
87	2022-10-25	1	1	deathwatch-vs-necrons-warhammer-40000-battle-report	\N	5
88	2022-10-22	2	1	seraphon-vs-hedonites-of-slaanesh-age-of-sigmar-battle-report	mkwsE7gXN6A	6
89	2022-10-21	1	2	grey-knights-vs-tau-empire-season-1-ep11-warhammer-40000-league-report	\N	4
100	2022-10-18	1	1	orks-vs-militarum-tempestus-warhammer-40000-battle-report	\N	4
101	2022-10-12	2	1	maggotkin-of-nurgle-vs-blades-of-khorne-age-of-sigmar-battle-report	\N	6
102	2022-10-11	1	1	drukhari-vs-imperial-knights-warhammer-40000-battle-report	\N	1
114	2022-09-09	1	4	fletchers-tau-empire-list-warhammer-40000-list-analysis	\N	\N
109	2022-10-08	2	1	slaves-to-darkness-vs-maggotkin-of-nurgle-age-of-sigmar-battle-report	Z83aXWZdYBU	3
116	2022-09-07	1	4	jinxs-tyranids-league-list-warhammer-40000-list-analysis	\N	\N
91	2022-10-07	1	2	iron-warriors-vs-necrons-season-1-ep9-warhammer-40000-league-report	\N	5
124	2022-08-18	1	4	the-bards-grey-knights-league-list-warhammer-40000-list-analysis	\N	\N
125	2022-08-17	1	4	beards-iron-warriors-league-list-warhammer-40000-list-analysis	\N	\N
128	2022-08-11	1	4	chefs-necrons-league-list-warhammer-40000-list-analysis	\N	\N
129	2022-08-10	1	4	spiders-flesh-tearers-league-list-warhammer-40000-list-analysis	\N	\N
104	2022-10-04	1	1	daemons-of-chaos-vs-black-templars-warhammer-40000-battle-report	\N	4
92	2022-09-30	1	2	iron-warriors-vs-tau-empire-season-1-ep8-warhammer-40000-league-report	\N	5
105	2022-09-28	2	1	new-age-of-sigmar-hedonites-of-slaanesh-vs-ossiarch-bonereapers-age-of-sigmar-battle-report	\N	6
106	2022-09-27	1	1	daemons-of-chaos-vs-orks-warhammer-40000-battle-report	\N	5
138	2023-03-29	2	1	sylvaneth-vs-maggotkin-of-nurgle-age-of-sigmar-battle-report	\N	6
137	2023-03-28	1	1	tau-empire-vs-genestealer-cults-warhammer-40000-battle-report	\N	4
115	2023-03-24	1	1	ultramarines-vs-necrons-warhammer-40000-battle-report	\N	1
103	2023-03-22	2	1	stormcast-eternals-vs-skaven-age-of-sigmar-battle-report	\N	4
84	2022-12-23	1	3	imperium-vs-orks-the-finale-warhammer-40000-narrative-report	\N	4
61	2022-12-10	2	1	idoneth-deepkin-vs-maggotkin-of-nurgle-age-of-sigmar-battle-report	PcYgrcu3Yik	6
64	2022-12-03	1	3	imperial-knights-vs-orks-warhammer-40000-narrative-report	wC5g7XIj1hk	6
68	2022-11-26	2	1	soulblight-gravelords-vs-ossiarch-bonereapers-age-of-sigmar-battle-report	Znt-NNmb1aw	5
71	2022-11-19	1	2	necrons-vs-tau-empire-season-1-ep15-warhammer-40000-league-report	UaD4tlrNT60	5
75	2022-11-12	1	1	new-codex-astra-militarum-vs-tyranids-warhammer-40000-battle-report	IrKqCC315jk	3
76	2022-11-11	1	2	flesh-tearers-vs-tyranids-season-1-ep14-warhammer-40000-league-report	\N	1
77	2022-11-09	2	1	soulblight-gravelords-vs-orruk-ironjawz-age-of-sigmar-battle-report	\N	3
78	2022-11-08	1	1	emperors-children-vs-adeptus-mechanicus-warhammer-40000-battle-report	\N	4
107	2022-09-24	2	1	new-age-of-sigmar-maggotkin-of-nurgle-vs-seraphon-age-of-sigmar-battle-report	\N	6
108	2022-09-24	2	1	new-age-of-sigmar-stormcast-eternals-vs-slaves-to-darkness-age-of-sigmar-battle-report	pKBEeZGZDvE	6
93	2022-09-23	1	2	tyranids-vs-necrons-season-1-ep7-warhammer-40000-league-report	\N	5
110	2022-09-20	1	1	aeldari-vs-iron-warriors-warhammer-40000-battle-report	\N	3
111	2022-09-17	1	1	new-codex-leagues-of-votann-vs-orks-warhammer-40000-battle-report	V-93P9LeoYU	3
94	2022-09-16	1	2	grey-knights-vs-tyranids-season-1-ep6-warhammer-40000-league-report	\N	3
112	2022-09-13	1	1	drukhari-vs-drukhari-warhammer-40000-battle-report	\N	4
113	2022-09-10	1	1	tallarn-vs-adepta-sororitas-warhammer-40000-battle-report	G1gvTLx4Kf4	5
95	2022-09-09	1	2	tyranids-vs-tau-empire-season-1-ep5-warhammer-40000-league-report	\N	6
96	2022-09-03	1	2	grey-knights-vs-necrons-season-1-ep4-warhammer-40000-league-report	xFEOWpaQr4	6
118	2022-09-02	1	1	emperors-children-vs-dark-angels-warhammer-40000-battle-report	\N	4
119	2022-08-30	1	1	chaos-daemons-vs-custodes-warhammer-40000-battle-report	\N	5
97	2022-08-26	1	2	flesh-tearers-vs-iron-warriors-warhammer-40000-league-report	\N	5
121	2022-08-23	1	1	tau-empire-vs-tyranids-warhammer-40000-battle-report	\N	6
122	2022-08-20	1	1	orks-vs-genestealer-cults-warhammer-40000-battle-reports	zToXYuPv4Sk	6
98	2022-08-19	1	2	grey-knights-vs-iron-warriors-warhammer-40000-league-report	\N	3
126	2022-08-16	1	1	aeldari-vs-tyranids-warhammer-40000-battle-report	\N	1
99	2022-08-13	1	2	all-new-league-necrons-vs-flesh-tearers-warhammer-40000-league-report	Fbyn0bovgrw	5
127	2022-08-12	1	1	space-marines-vs-adeptus-mechanicus-warhammer-40000-battle-report	\N	1
130	2022-08-09	1	1	orks-vs-adepta-sororitas-2000pts-warhammer-40000-battle-report-3	\N	3
131	2022-08-06	1	1	thousand-sons-vs-aeldari-2000pts-warhammer-40000-battle-report	ng2nslwMAc8	5
132	2022-08-05	1	1	dark-angels-vs-alpha-legion-2000pts-warhammer-40000-battle-report	\N	5
133	2022-08-02	1	1	grey-knights-vs-death-guard-2000pts-warhammer-40000-battle-report	\N	4
134	2022-07-30	1	1	adeptus-custodes-vs-aeldari-2000pts-warhammer-40000-battle-report	X-pIcBO-PSo	5
135	2022-07-29	1	1	grey-knights-vs-harlequins-warhammer-40000-battle-report	\N	4
136	2022-07-26	1	1	tau-empire-vs-adepta-sororitas-2000pts-warhammer-40000-battle-report	\N	3
139	2022-07-25	1	1	imperial-knights-vs-chaos-knights-2000pts-warhammer-40000-battle-report-2	\N	1
140	2022-07-23	1	1	white-scars-vs-orks-2000pts-warhammer-40000-battle-report	GTECL7JBQPQ	4
141	2022-07-19	1	3	flesh-tearers-vs-necrons-warhammer-40000-narrative-report	\N	5
142	2021-12-21	1	3	flesh-tearers-vs-necrons-1500pts-warhammer-40000-narrative-report	\N	1
144	2023-04-01	1	1	iron-warriors-vs-imperial-fists-boarding-action-battle-report	KhiG8VQ3amY	\N
90	2022-10-15	1	2	flesh-tearers-vs-tau-empire-season-1-ep10-warhammer-40000-league-report	mr1bd3aHqyE	5
51	2022-10-14	1	3	astra-militarum-vs-orks-s1-ep2-warhammer-40000-narrative-report	\N	6
120	2022-08-27	1	1	new-codex-chaos-daemons-vs-grey-knights-warhammer-40000-battle-report	FNLvZlyJnks	6
152	2022-07-05	1	1	dark-angels-vs-drukhari-2000pts-warhammer-40000-battle-report	\N	3
159	2023-04-14	1	2	astra-militarum-vs-aeldari-season-2-ep-7-warhammer-40000-league-report	\N	1
153	2022-07-02	1	1	iron-warriors-vs-emperors-children-2000pts-warhammer-40000-battle-report	Cv3xkqoi-hk	5
81	2022-10-29	1	1	chaos-daemons-vs-leagues-of-votann-warhammer-40000-battle-report	DtQxvZ910Gw	6
145	2022-07-16	1	1	creations-of-bile-vs-tau-empire-warhammer-40000-battle-report	WSh3X1rHYF	3
150	2023-04-04	1	1	adeptus-custodes-vs-harlequins-warhammer-40000-battle-report	\N	5
143	2023-03-31	1	2	craftworld-aeldari-vs-leagues-of-votann-season-2-ep-5-warhammer-40000-league-report	\N	5
123	2023-03-25	1	2	astra-militarum-vs-leagues-of-votann-season-2-ep-4-warhammer-40000-league-report	3lk_rDVyDQc	3
154	2023-03-21	1	1	white-scars-vs-imperial-knights-warhammer-40000-battle-report	\N	4
2	2023-03-04	1	2	thousand-sons-vs-craftworld-aeldari-season-2-ep-1-warhammer-40000-league-report	aQq6qKfM6TM	6
155	2023-04-07	1	2	adeptus-mechanicus-vs-aeldari-season-2-ep-6-warhammer-40000-league-report	\N	5
37	2023-01-17	1	1	adeptus-mechanicus-vs-chaos-knights-warhammer-40000-battle-report	\N	4
156	2023-04-08	2	1	new-battletomes-soulblight-gravelords-vs-ossiarch-bonereapers-age-of-sigmar-battle-report	L-b7lN1CXDo	5
49	2022-12-24	1	2	flesh-tearers-vs-necrons-season-1-ep20-the-final-warhammer-40000-league-report	eODR7BKmQIQ	1
157	2023-04-11	1	1	chaos-daemons-vs-world-eaters-warhammer-40000-battle-report	\N	4
158	2023-04-12	2	1	ironjawz-vs-nighthaunt-age-of-sigmar-battle-report	\N	4
146	2022-07-15	1	1	adeptus-mechanicus-vs-tyranids-2000pts-warhammer-40000-battle-report	\N	1
147	2022-07-12	1	1	astra-militarum-vs-necrons-2000pts-warhammer-40000-battle-report	\N	4
149	2022-07-09	1	3	genestealer-cults-vs-ultramarines-warhammer-40000-narrative-report	f8lsX6Yw1VU	4
151	2022-07-08	1	1	world-eaters-vs-adeptus-mechanicus-2000pts-warhammer-40000-battle-report	\N	4
148	2022-04-29	1	3	genestealer-cults-vs-ultramarines-1750pts-warhammer-40000-narrative-report	\N	4
160	2022-07-01	1	1	imperial-fists-vs-iron-warriors-2000pts-warhammer-40000-battle-report-2	\N	5
161	2022-06-28	1	1	genestealer-cults-vs-emperors-children-2000pts-warhammer-40000-battle-report	\N	4
162	2022-06-25	1	1	new-codex-chaos-space-marines-vs-ultramarines-2000pts-warhammer-40000-battle-report	CMNuOyYw-2Q	3
163	2022-06-24	1	1	drukhari-vs-grey-knights-2000pts-warhammer-40000-battle-report	\N	4
165	2022-06-21	1	3	astra-militarum-vs-tyranids-warhammer-40000-narrative-report	\N	6
166	2022-06-18	1	1	adeptus-custodes-vs-necrons-2000pts-warhammer-40000-battle-report	WJ7x56XpQeU	6
167	2022-06-17	1	1	asuryani-vs-drukhari-2000pts-warhammer-40000-battle-report	\N	5
168	2023-04-15	1	1	dark-angels-vs-world-eaters-warhammer-40000-battle-report	Ai11yOyMVwM	4
169	2022-06-14	1	1	imperial-knights-vs-salamanders-2000pts-warhammer-40000-battle-report	\N	3
170	2022-06-11	1	1	ulthwe-vs-adepta-sororitas-2000pts-warhammer-40000-battle-report	3xnCb6CyC5w	4
164	2022-02-04	1	3	tyranids-vs-astra-militarum-1750pts-warhammer-40000-narrative-report	\N	1
171	2022-06-10	1	1	imperial-fists-vs-orks-2000pts-warhammer-40000-battle-report	\N	4
172	2022-06-07	1	2	ynnari-vs-chaos-knights-2000pts-warhammer-40000-league-report	\N	5
173	2022-01-15	1	3	space-marines-vs-thousand-sons-1750pts-warhammer-40000-narrative-report	HQVNAuR4O00	4
175	2022-06-03	1	1	adepta-sororitas-vs-militarum-tempestus-2000pts-warhammer-40000-battle-report	\N	1
176	2023-04-17	1	1	drukhari-vs-leagues-of-votann-warhammer-40000-battle-report	\N	4
177	2023-04-19	1	1	death-guard-vs-astra-militarum-boarding-action-battle-report	\N	\N
178	2022-05-31	1	1	necrons-vs-deathwatch-2000pts-warhammer-40000-battle-report-2	\N	5
174	2022-06-04	1	3	thousand-sons-vs-obsidian-dragons-1750pts-warhammer-40000-narrative-report	i8-wvip7CuQ	5
179	2022-05-28	1	2	death-guard-vs-adeptus-mechanicus-2000pts-warhammer-40000-league-report-2	XtOIlYfNGm0	5
180	2023-04-21	1	1	tyranids-vs-adepta-sororitas-warhammer-40000-battle-report-3	\N	5
181	2022-05-27	1	2	tyranids-vs-adeptus-mechanicus-2000pts-warhammer-40000-league-report-2	\N	5
182	2022-05-24	1	1	tau-empire-vs-ultramarines-2000pts-warhammer-40000-battle-report-2	\N	6
183	2022-05-21	1	1	grey-knights-vs-tyranids-2000pts-warhammer-40000-battle-report	xg0AGpEWBVo	3
184	2023-04-19	1	2	orks-vs-astra-militarum-season-2-ep-8-warhammer-40000-league-report	tTbrnKS7keo	3
185	2023-04-25	1	1	iron-warriors-vs-drukhari-warhammer-40000-battle-report	\N	4
186	2022-05-20	1	2	flesh-tearers-vs-tau-empire-2000pts-warhammer-40000-league-report	\N	4
187	2022-05-17	1	1	chaos-knights-vs-tau-empire-2000pts-warhammer-40000-battle-report	\N	6
188	2022-05-14	1	1	new-codex-imperial-knights-vs-adeptus-custodes-2000pts-warhammer-40000-battle-report	ctIGycBhV_U	4
189	2022-05-13	1	1	chaos-knights-vs-adeptus-mechanicus-2000pts-warhammer-40000-battle-report	\N	6
190	2022-05-10	1	1	new-codex-imperial-knights-vs-orks-2000pts-warhammer-40000-battle-report	\N	6
191	2022-05-07	1	1	new-codex-chaos-knights-vs-dark-angels-2000pts-warhammer-40000-battle-report	5nRDg5cGHO4	4
192	2023-04-25	2	1	stormcast-eternals-vs-hedonites-of-slaanesh-age-of-sigmar-battle-report	\N	3
193	2022-05-06	1	2	death-guard-vs-emperors-children-2000pts-warhammer-40000-league-report	\N	4
194	2022-05-03	1	1	dark-angels-vs-craftworlds-2000pts-warhammer-40000-battle-report	\N	3
195	2022-04-30	1	1	tyranids-vs-ultramarines-2000pts-warhammer-40000-battle-report	1gU5Z7w-5eM	6
196	2022-04-26	1	1	black-templars-vs-death-guard-2000pts-warhammer-40000-battle-report	\N	6
197	2023-04-28	1	2	thousand-sons-vs-leagues-of-votann-season-2-ep-9-warhammer-40000-league-report	\N	5
198	2022-04-23	1	1	white-scars-vs-thousand-sons-2000pts-warhammer-40000-league-report	rFAsEkGsZsg	6
199	2022-04-22	1	2	ynnari-vs-grey-knights-2000pts-warhammer-40000-league-report	\N	1
200	2023-05-02	1	2	adeptus-mechanicus-vs-orks-season-2-ep-10-warhammer-40000-league-report	\N	3
201	2023-05-03	2	1	new-battletome-ossiarch-bonereapers-vs-seraphon-age-of-sigmar-battle-report	\N	5
202	2023-05-05	1	2	aeldari-vs-orks-season-2-ep-11-warhammer-40000-league-report	\N	5
\.


--
-- Data for Name: showtypes; Type: TABLE DATA; Schema: public; Owner: philip
--

COPY public.showtypes (id, showtype) FROM stdin;
1	Battle report
2	League report
3	Narrative report
4	List analysis
\.


--
-- Data for Name: subfactions; Type: TABLE DATA; Schema: public; Owner: philip
--

COPY public.subfactions (id, subfaction, faction_id) FROM stdin;
1	Dark Angels	1
2	Solar Watch	2
3	Cult of Duplicity	3
4	Ulthwé	4
5	Goffs	7
6	Vyrkos	9
7	Coalesced	8
8	Deathskulls	7
9	World Eaters	11
10	Flesh Tearers	1
11	Emperor's Chosen	2
12	Cult of Strife	15
13	Deathwatch	1
14	Ymyr Conglomerate	18
15	Host of the Everchosen	19
16	Farsight Enclaves	20
17	Hammers of Sigmar	21
18	Pretenders	22
19	Petrifex Elite	24
20	Crimson Fists	1
21	Evil Sunz	7
22	Ultramarines	1
23	Red Corsairs	27
24	Fuethán	23
25	Emerald Host	28
26	Emissaries Imperatus	2
27	Ironjawz	29
28	Emperor's Children	27
29	Iron Hands	1
30	Iron Warriors	27
31	Black Legion	27
32	Stalliarch Lords	24
33	Ionrach	23
34	Lucius	25
35	House Herpetrax	30
36	Swordbearers	6
37	Order of the Valorous Heart	31
38	Behemoth	32
39	Salamanders	1
40	Kabal of the Poisoned Tongue	15
41	Heartwood	34
42	Iyanden	4
43	House Terryn	26
44	Despoilers	19
45	Kronos	32
46	Biel-Tan	4
47	Novokh	16
48	Obsekh Dynasty	16
49	Invaders	22
50	Order of the Ebon Chalice	31
51	Black Templars	1
52	Bloodlords	35
53	Befouling Host	12
54	Leviathan	32
55	Greater Thurian League	18
56	House Krast	26
57	Nautilar	23
58	Twisted Helix	36
59	The Inexorable	33
60	Hallowed Knights	21
61	Bork'an	20
62	Legion of Blood	9
63	Boulderhead	13
64	Godseekers	22
65	Cabalists	19
66	Celestial Warbringers	21
67	Mephrit	16
68	Blood Axes	7
69	Cult of the Cursed Blade	15
70	House Taranis	26
71	Clans Pestilens	37
72	Crematorians	24
73	Ravagers	19
74	Trans-Hyperian Alliance	18
75	Kabal of the Obsidian Rose	15
76	Order of Our Martyred Lady	31
77	Nephrekh	16
78	Metalica	25
79	Blades of Victory	6
80	Jormungandr	32
81	Cult of the Four-armed Emperor	36
82	Hydra	32
83	Raven Guard	1
84	Order of the Argent Shroud	31
85	Alpha Legion	27
86	Mortarion's Anvil	33
87	Wardmakers	6
88	Dread Host	2
89	Dark	38
90	Prescient Brethren	6
91	Sa'cea	20
92	Rusted Claw	36
93	House Griffith	26
94	White Scars	1
95	Imperial Fists	1
96	Creations of Bile	27
97	Mars	25
98	Twilight	38
99	Ryza	25
100	Mortis Praetorians	24
101	Rapiers	2
102	Saim-Hann	4
103	Ynnari	4
104	Cult of Time	3
105	Kabal of the Black Heart	15
106	Kraken	32
107	House Raven	26
108	House Korvax	30
109	Rapiers	6
\.


--
-- Name: armies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: philip
--

SELECT pg_catalog.setval('public.armies_id_seq', 390, true);


--
-- Name: campaigns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: philip
--

SELECT pg_catalog.setval('public.campaigns_id_seq', 6, true);


--
-- Name: factions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: philip
--

SELECT pg_catalog.setval('public.factions_id_seq', 38, true);


--
-- Name: games_id_seq; Type: SEQUENCE SET; Schema: public; Owner: philip
--

SELECT pg_catalog.setval('public.games_id_seq', 2, true);


--
-- Name: leagueseasons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: philip
--

SELECT pg_catalog.setval('public.leagueseasons_id_seq', 31, true);


--
-- Name: narrativeshows_id_seq; Type: SEQUENCE SET; Schema: public; Owner: philip
--

SELECT pg_catalog.setval('public.narrativeshows_id_seq', 18, true);


--
-- Name: players_id_seq; Type: SEQUENCE SET; Schema: public; Owner: philip
--

SELECT pg_catalog.setval('public.players_id_seq', 17, true);


--
-- Name: shows_id_seq; Type: SEQUENCE SET; Schema: public; Owner: philip
--

SELECT pg_catalog.setval('public.shows_id_seq', 202, true);


--
-- Name: showtypes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: philip
--

SELECT pg_catalog.setval('public.showtypes_id_seq', 4, true);


--
-- Name: subfactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: philip
--

SELECT pg_catalog.setval('public.subfactions_id_seq', 109, true);


--
-- Name: armies armies_pkey; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.armies
    ADD CONSTRAINT armies_pkey PRIMARY KEY (id);


--
-- Name: campaigns campaigns_pkey; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.campaigns
    ADD CONSTRAINT campaigns_pkey PRIMARY KEY (id);


--
-- Name: factions factions_faction_game_id_unq; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.factions
    ADD CONSTRAINT factions_faction_game_id_unq UNIQUE (faction, game_id);


--
-- Name: factions factions_pkey; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.factions
    ADD CONSTRAINT factions_pkey PRIMARY KEY (id);


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (id);


--
-- Name: leagueseasons leagueseasons_league_season_episode; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.leagueseasons
    ADD CONSTRAINT leagueseasons_league_season_episode UNIQUE (league_season, episode);


--
-- Name: leagueseasons leagueseasons_pkey; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.leagueseasons
    ADD CONSTRAINT leagueseasons_pkey PRIMARY KEY (id);


--
-- Name: narrativeshows narrativeshows_campaign_id_campaign_sequence_unq; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.narrativeshows
    ADD CONSTRAINT narrativeshows_campaign_id_campaign_sequence_unq UNIQUE (campaign_id, campaign_sequence);


--
-- Name: narrativeshows narrativeshows_pkey; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.narrativeshows
    ADD CONSTRAINT narrativeshows_pkey PRIMARY KEY (id);


--
-- Name: players players_pkey; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (id);


--
-- Name: shows shows_pkey; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.shows
    ADD CONSTRAINT shows_pkey PRIMARY KEY (id);


--
-- Name: showtypes showtypes_pkey; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.showtypes
    ADD CONSTRAINT showtypes_pkey PRIMARY KEY (id);


--
-- Name: subfactions subfactions_pkey; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.subfactions
    ADD CONSTRAINT subfactions_pkey PRIMARY KEY (id);


--
-- Name: subfactions subfactions_subfaction_faction_id; Type: CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.subfactions
    ADD CONSTRAINT subfactions_subfaction_faction_id UNIQUE (subfaction, faction_id);


--
-- Name: armies_faction_id_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX armies_faction_id_idx ON public.armies USING btree (faction_id);


--
-- Name: armies_player_id_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX armies_player_id_idx ON public.armies USING btree (player_id);


--
-- Name: armies_show_id_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX armies_show_id_idx ON public.armies USING btree (show_id);


--
-- Name: armies_subfaction_id_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX armies_subfaction_id_idx ON public.armies USING btree (subfaction_id);


--
-- Name: campaigns_campaign_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE UNIQUE INDEX campaigns_campaign_idx ON public.campaigns USING btree (campaign);


--
-- Name: factions_faction_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX factions_faction_idx ON public.factions USING btree (faction);


--
-- Name: factions_game_id_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX factions_game_id_idx ON public.factions USING btree (game_id);


--
-- Name: games_game_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE UNIQUE INDEX games_game_idx ON public.games USING btree (game);


--
-- Name: leagueseasons_episode_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX leagueseasons_episode_idx ON public.leagueseasons USING btree (episode);


--
-- Name: leagueseasons_league_season_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX leagueseasons_league_season_idx ON public.leagueseasons USING btree (league_season);


--
-- Name: leagueseasons_show_id_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE UNIQUE INDEX leagueseasons_show_id_idx ON public.leagueseasons USING btree (show_id);


--
-- Name: narrativeshows_campaign_id_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX narrativeshows_campaign_id_idx ON public.narrativeshows USING btree (campaign_id);


--
-- Name: narrativeshows_campaign_sequence_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX narrativeshows_campaign_sequence_idx ON public.narrativeshows USING btree (campaign_sequence);


--
-- Name: narrativeshows_show_id_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE UNIQUE INDEX narrativeshows_show_id_idx ON public.narrativeshows USING btree (show_id);


--
-- Name: players_fullname_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE UNIQUE INDEX players_fullname_idx ON public.players USING btree (fullname);


--
-- Name: players_nickname_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE UNIQUE INDEX players_nickname_idx ON public.players USING btree (nickname);


--
-- Name: shows_game_id_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX shows_game_id_idx ON public.shows USING btree (game_id);


--
-- Name: shows_release_date_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX shows_release_date_idx ON public.shows USING btree (release_date);


--
-- Name: shows_servoskull_id_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX shows_servoskull_id_idx ON public.shows USING btree (servoskull_id);


--
-- Name: shows_showtype_id_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX shows_showtype_id_idx ON public.shows USING btree (showtype_id);


--
-- Name: shows_slug_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE UNIQUE INDEX shows_slug_idx ON public.shows USING btree (slug);


--
-- Name: shows_youtube_slug_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE UNIQUE INDEX shows_youtube_slug_idx ON public.shows USING btree (youtube_slug);


--
-- Name: showtypes_showtype_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE UNIQUE INDEX showtypes_showtype_idx ON public.showtypes USING btree (showtype);


--
-- Name: subfactions_faction_id_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX subfactions_faction_id_idx ON public.subfactions USING btree (faction_id);


--
-- Name: subfactions_subfaction_idx; Type: INDEX; Schema: public; Owner: philip
--

CREATE INDEX subfactions_subfaction_idx ON public.subfactions USING btree (subfaction);


--
-- Name: armies armies_faction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.armies
    ADD CONSTRAINT armies_faction_id_fkey FOREIGN KEY (faction_id) REFERENCES public.factions(id);


--
-- Name: armies armies_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.armies
    ADD CONSTRAINT armies_player_id_fkey FOREIGN KEY (player_id) REFERENCES public.players(id);


--
-- Name: armies armies_show_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.armies
    ADD CONSTRAINT armies_show_id_fkey FOREIGN KEY (show_id) REFERENCES public.shows(id);


--
-- Name: armies armies_subfaction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.armies
    ADD CONSTRAINT armies_subfaction_id_fkey FOREIGN KEY (subfaction_id) REFERENCES public.subfactions(id);


--
-- Name: factions factions_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.factions
    ADD CONSTRAINT factions_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(id);


--
-- Name: leagueseasons leagueseasons_show_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.leagueseasons
    ADD CONSTRAINT leagueseasons_show_id_fkey FOREIGN KEY (show_id) REFERENCES public.shows(id);


--
-- Name: narrativeshows narrativeshows_campaign_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.narrativeshows
    ADD CONSTRAINT narrativeshows_campaign_id_fkey FOREIGN KEY (campaign_id) REFERENCES public.campaigns(id);


--
-- Name: narrativeshows narrativeshows_show_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.narrativeshows
    ADD CONSTRAINT narrativeshows_show_id_fkey FOREIGN KEY (show_id) REFERENCES public.shows(id);


--
-- Name: shows shows_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.shows
    ADD CONSTRAINT shows_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(id);


--
-- Name: shows shows_servoskull_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.shows
    ADD CONSTRAINT shows_servoskull_id_fkey FOREIGN KEY (servoskull_id) REFERENCES public.players(id);


--
-- Name: shows shows_showtype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.shows
    ADD CONSTRAINT shows_showtype_id_fkey FOREIGN KEY (showtype_id) REFERENCES public.showtypes(id);


--
-- Name: subfactions subfactions_faction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: philip
--

ALTER TABLE ONLY public.subfactions
    ADD CONSTRAINT subfactions_faction_id_fkey FOREIGN KEY (faction_id) REFERENCES public.factions(id);


--
-- PostgreSQL database dump complete
--

