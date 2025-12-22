---
title: '--- Enhanced Notes ---'
date: '2025-12-18'
time: '14:41'
attendees:
- -- Enhanced Notes ---
- '### Current Claude/AI Development Excitement'
- Both feeling transported back 15-20 years to early programming days
- Similar excitement to when Sergi started with Google Ads in 2005
- "Peter feels like he\u2019s rediscovered the joy of coding"
- Everything feels possible now with modern web development technologies
- Node.js, Express Server, Flask apps
- Cloud deployment via Railway for web server hosting
- "### Peter\u2019s Recipe Card Project"
- Built system to digitize Gusto meal kit recipe cards
- Takes photos of front/back of cards
- Extracts text automatically into searchable format
- "Kids can search by ingredients (e.g., \u201Ccourgette and chicken\u201D)"
- Demonstrates rapid development capability - completed in \~30 minutes
- Planning web deployment via Railway cloud platform
- '### Development Workflow Preferences'
- Peter uses raw terminal screen with Claude
- Prefers text-based interface over formatted chat
- Uses bypass permissions flag to avoid constant prompts
- Often runs 2-3 hour development sessions
- Sergi primarily uses chat interface
- Finds prompts manageable for smaller batches
- Typically works in 5-minute increments
- "### Peter\u2019s Advanced AI Knowledge Base System"
- Building comprehensive brain dump system
- Pulls from Google dev blog, industry experts (Brad Geddes, Frederick Vallaeys)
- Updates weekly, monthly, quarterly, yearly
- Indexes content properly using SQLite
- Strategic decision support
- Analyzes context for Google Ads optimization decisions
- Suggests alternatives based on knowledge base
- Acts like having an apprentice
- Integration with Google Ads management
- Writes strategy reports and client communications
- Implements changes directly via API
- Includes mandatory validation protocols (backup, dry run, verify, restore)
- '### Advanced Google Ads Automation'
- Asset text optimization system
- Pulls headlines/descriptions from PMAX campaigns
- Analyzes 90-day performance (CTR focus)
- Categorizes underperforming assets
- Generates 15 alternative text options with dropdown selection
- Experiment tracking system
- Logs all changes with expectations
- Creates follow-up tasks for 4-week reviews
- Provides categorical success/failure analysis
- 'Client example: $9 million Q4 US sales for toy client'
- Handles rapid budget changes during peak season
- Automates email responses and change documentation
- "### Sergi\u2019s Productivity Systems"
- Live audit system
- Reduces audit time from 6-7 hours to 30 minutes
- Built from scratch rather than using existing templates
- Meeting preparation automation
- Pulls from Slack, emails, meeting notes
- Generates formatted Google Slides with client logos
- 10-minute prep vs 2-3 hours manual work
- Automated reminder system
- Scans communications every couple hours
- Sends Slack notifications for tasks/reminders
- Integrates with custom dashboard for approval/deletion
- '### Dashboard and Task Management'
- "Sergi\u2019s comprehensive client dashboard"
- Task management synced with Google Sheets
- Client engagement scoring system (60-90 points weekly)
- Health monitoring for caches and systems
- Engagement gamification
- Points for calls (30), emails (varies), Slack messages (5), Google Ads changes (3)
- Adjustable targets based on client payment/demands
- Red zone alerts for neglected accounts
- Template workflows for recurring tasks (promos, sales periods)
- '### Technical Integration Challenges'
- MCP server implementations
- Shopify integration working (requires app setup)
- WooCommerce integration functional
- Google Trends problematic (timeouts, API limits)
- API cost management
- Claude Max covers cursor usage
- Separate Anthropic API costs for independent agents
- Recommendation to use Haiku for cost efficiency
- Skills vs API limitations
- Web UI cannot access cursor skills
- Forced return to terminal interface for full functionality
- --
- 'Chat with meeting transcript: [https://notes.granola.ai/t/86d253a0-72f5-4a7a-bb96-87e3237ba898](https://notes.granola.ai/t/86d253a0-72f5-4a7a-bb96-87e3237ba898)'
- -- Full Transcript ---
- 'Me: Hey, segi.'
- 'Them: Hi, peter. Hello.'
- 'Me: Yeah. Good.'
- 'Them: Yeah. Good.'
- 'Me: I''ve got. It''s Friday, I must say.'
- 'Them: Yeah, well.'
- 'Me: So tired.'
- 'Them: How''s it going?'
- 'Me: I feel like I''ve been transported back about. 20 years, 25 years back to being
  a programmer. And being excited about code, and so I''ve not been able to walk away
  from your desk.'
- 'Them: Look, I didn''t say 25. I was thinking 15.'
- 'Me: Oh, okay. Thank you very much for that. I appreciate that.'
- 'Them: Thousand. Well, I''ll get. Fine. Didn''t sound the way it went, but anyway,
  I thought exactly the same. I thought exactly the same. Right. I was thinking about
  it just 10 minutes ago. I was thinking, how do I feel about this? And I was thinking,
  it feels like the self excitement I had. Well, I say 15, but actually now it''s
  more 20, because 15 is when I got into Google Ads. Yeah, that''s the sort of thing
  I got back 2005. When I. I started playing up with java. And, you know, and all
  these things, you know, getting deep into programming, and that was actually.'
- 'Me: When you''ve enjoyed it. When you enjoy doing it as well. That''s the thing
  that gave me the buzz.'
- 'Them: Yeah, yeah, yeah, yeah.'
- 'Me: I''m glad you feel the same. That''s brilliant.'
- 'Them: Exactly, exactly the same. And. And actually thinking back, so before starting
  at Success, that was obviously on my own, doing work for five, six, six clients.
  I was thinking. Look, this is not going anywhere. I''m not really loving it. I know.
  You spend four very intense months. Learning about Node Lending, about Express Server.
  So all these web development technologies that have been, you know, created, that
  were new. That didn''t exist. When I was building, you know, from its clothes, so
  to speak. 15, 20 years ago. So now, obviously, everything has changed now.'
- 'Me: Yeah.'
- 'Them: And everything is possible now.'
- 'Me: Absolutely right. Absolutely right. Everything is possible. That''s a really
  good way to describe it. It''s really strange. Isn''t it? I''m using. What''s a
  flask app? I have no idea. I don''t know what railway is. Railways to run an app
  on it on a web server. So you can run a cloud app on a web server and access it
  anywhere. Yeah.'
- 'Them: Do you think my way? I started using my weight yesterday. Yeah, yeah.'
- 'Me: So. And it was a crazy thing. I said, we have. It''s got to be called gusto.
  I don''t know whether you were aware of it in the UK when you were in the UK with
  you had it or not, but basically they provide the menus and the ingredients. For
  meals. So you say, right? I want to buy four meals. I want this one, this one, this
  one and this one. They send you the fresh vegetables and all the rest in a box.
  With all the meat. All the rest of them come with four cards. If you got four recipes
  and you follow the recipe on it. And it''s fabulous food, absolute, like, techniques
  you wouldn''t normally use. It''s not cheap, but it''s really good with eating some
  fantastic stuff, even though it''s a good cook. Anyway, it''s different stuff. So
  I thought, okay. What if I took a pitcher of the front and the back of that card?
  Made it into a recipe and then put it on the web and made it searchable. And then
  the kids could access all those recipes. So you could say I''ve got courgette and
  chicken. What have you got with courgette and chicken? In and it would go and pop
  up the recipes. Yeah, done that. So actually taking a photo of it front and back,
  it reads it, it puts it into the right sort of floor mat and it puts it onto the
  Internet. I''ve not got the Internet bit yet because I''ve not got the railway bit,
  but that was like half an hour.'
- 'Them: Sorry. Are we talking about pushing recipes? Sorry I lost you there. I thought
  it was. It was as it was an example. And then I realized you were talking about
  real thing.'
- 'Me: Yeah. It was a real thing. Yeah. So we got these cards, these recipe cards.
  That from Gusto, I thought, take a picture the front and back of them. And there''s
  photos on there, there''s all sorts, but I just wanted to get the text of it. And
  they''re in the same format. It''s got the nutrition on there. It serves this many.
  And then it''s got the actual process, but it''s got a list of all the ingredients.
  Above it. So I''m going to put that onto a web server. So that the kids can go onto
  that web server, given the password, and they can go look for these recipes.'
- 'Them: Okay?'
- 'Me: So they''re all searchable. And it was just a bit of fun. And this is like
  you got your four things running. You think, well, I''ve got a spare one there,
  let''s do it on there.'
- 'Them: Yeah, he''s like a waste if you like. I mean, you have three screens, so
  why not have three things building at the same time? I have all this chat tabs and
  I have two, three working at the same time. I sometimes think, well, why don''t
  I have a fourth one? And I''m building something else.'
- 'Me: Something for a bit of fun, yeah?'
- 'Them: Right. For fun. For fun.'
- 'Me: Now, the interesting bit is, okay, so actual technique there. Do you use terminal?
  Do you use chat? On cursor.'
- 'Them: I mostly chat. Very rarely I need to use terminal.'
- 'Me: So I use the raw terminal screen. I''ll just type Claude into when it pops
  up. Type Claude in it, does it? It''s not. It''s the pure text version. There is
  the chat version, isn''t there? Which is a little bit more formatted. I don''t actually
  use that anymore.'
- 'Them: Sorry. By the way, this one? I said five. Okay, go ahead. Here.'
- 'Me: So if you call it terminal, in chat, in cursor. So the one thing I''ve done
  is I started up doing Claude. So I just run claws and it pops up and you can go
  and use Claude in it. So then I''ve done. What Mike''s done is using the abbreviations.
  And done the version where. What''s the name of it? There''s the flag which says
  ignore any sort of input at all. Just run it. And it just blasts its way. I can''t
  remember what it''s called now.'
- 'Them: Composite.'
- 'Me: No. Damn it. What was it? I''m normally talking into this. It''s weird typing.
  Because normally it''ll prompt you, wouldn''t it? It said, do you want to use Bash?
  Do you want to do this? So you can actually set the flag that just goes. And it
  just blasts through it.'
- 'Them: This is not what you explained the other day. How did you call it?'
- 'Me: ''s a really weird.'
- 'Them: Can you tell? Very composer.'
- 'Me: No. It''s a flag to use with Claude. When I find it, I''ll let you know.'
- 'Them: You asked for a feature or something, you enter the prompt and what would
  normally happen is that it would ask you confirmation to things.'
- 'Me: Correct.'
- 'Them: Sometimes you get yes. No. Sometimes you get yes. Sometimes you get yes to
  everything like that.'
- 'Me: Yeah. One, two or three? Two. And one and. Yeah. Make sure you''re awake. Yes.'
- 'Them: I normally go at some point. Maybe the first part, they say yes. And the
  second one, when I know it''s going in the right direction, I go yes to everything.
  And then I move on. I come back five minutes later.'
- 'Me: Yeah, there''s another. There''s another version of Claude where you can run
  it with a flag. And basically you just leave it. You say, I want to do this, this,
  this, this and this. And it goes. And it just rattles it off. And there''s very
  few prompts. You got to be careful with it. It''s actually doing the right thing.'
- 'Them: Okay? Yeah, I. Don''t find I don''t find the prompts, I don''t find I get
  too many problems. I don''t think I''m being delayed. I mean, it''s not like. Look,
  we have to build this today point, okay? The client is like, okay, fine.'
- 'Me: Yeah.'
- 'Them: If I get. Look, I don''t think we''ll make. I mean, if I''m the scientist
  correctly, I don''t find it particularly annoying that I get prompts from time to
  time. And when I get the option, normally just go for yes to everything and it leaves
  me alone. And to be honest, I work in a small batches, so it''s not like I want.
  I mean, I don''t expect to add a prompt. I will require an hour''s work. For Claude.
  Normally within five minutes.'
- 'Me: Oh, gosh, I''ve been to two or three hours.'
- 'Them: The time.'
- 'Me: Just on one thing. When I''m planning something, I''ll just put two or three
  hours. It''ll just go and do it.'
- 'Them: Okay? Okay, let''s go. Okay, let''s go. Where are you building that will
  require two, three hours of work every day.'
- 'Me: I''m building my brain, Sergey. That''s what I''m doing. I''m building my brain.
  Okay?'
- 'Them: I wish you.'
- 'Me: I''ll give you an example. I''ll give you an example. So I''ve got a knowledge
  base. Right. I''m at a stage now where Mike produces something in his brain. And
  I''ll pull it in and I''ll say, what''s in Mike''s brain that I could put into mine.
  And I''ve got to the point now. He said nothing. Yeah. There''s nothing that you
  can do. There''s nothing you can add from Mike''s brain to yours where he''s doing
  it better. Because the thing with Mike is. And that''s not an ego thing. He isn''t
  running an agency. A lot of the stuff he does isn''t agency stuff. And when he goes
  and does the CSV analyzer is very good. I really like that one. That is very good.
  But most of the other stuff, like where he''s doing the search terms, I''ll put
  it into high and medium, low intent. You just go, yeah. 20 and it''s got tired.
  It couldn''t do anymore. Well, I''ve got 100,000 in there. What am I supposed to
  do with those? How am I supposed to categorize those? If you want to do over a big
  period of time and make it worth your while. So I don''t tend to do touches. But
  one thing I did do at the beginning was I wanted a knowledge base. The key to their
  brain is that we are doing a brain dump. We''re actually saying, these are all the
  things that I know. These are all the things that the Internet knows about what
  I know, what I do. I want to put them all into a knowledge base. And I want to keep
  that up to date. I want to be looking at the Google dev blog on a regular basis,
  see if there''s anything on there that''s interesting that I might find interesting
  and bring it in. It''s something Brad Geddes is doing that''s interesting. Frederick
  Valets what they talk about search engine life, all those. So I started doing that,
  and I pulled in. I said, go and find me some websites with Providence and people
  with Providence and pull it all into a database. Mike then was talking about his
  brain was talking about using SQ Light for doing indexing. So it will actually index
  it properly. And then I took it at stage further. The other day. It''s like taking
  a stronger and stronger drug, isn''t it? You just push it a little bit more. So
  now the knowledge base will update every week, every month, every quarter and every
  year. And it will basically mash it all together, all the stuff that''s being talked
  about. And I can either search it and say, what''s the latest thinkings on pmax
  optimization? Or I''ve got it now and I''m still not sure how it''s going to work
  this because we literally finished yesterday. But when I make a decision, a strategic
  decision in Google Ads to say, I''m going to do this on this client, it will then
  go look at the knowledge base and say, I''ve got this context about that. And maybe
  you want to try this or maybe you want to try that. That''s what I''m aiming towards.
  But it''s like having all of it is like having an apprentice. And you say, can you
  go and do that? And you go and give it some work to do. And it comes back and you
  read it and go. And I''ve said it to before, that''s rubbish. That''s absolutely
  rubbish. Because of this, this and this. You''re absolutely right. I''m fed up with
  it saying that, but you''re absolutely right. I didn''t do this. Or I didn''t do
  that. I''d done a report for a client and it was completely wrong. And he said,
  well, I didn''t really wanted the latest data. What do you mean? Well, yeah. Then
  you build stuff in like that. I''m now using it. So you said the top five, but they''re
  all kind of blended together. But I got it to a point now where I''m writing stuff
  back to Google. So I''ve got a client now where there''s some big budget changes,
  so I''ve done a Q4 strategy report for it. And then said, give me that strategy.
  Let''s go and look at it. We find all the strategy when the budget changes need
  to be based upon last year''s conversion rate increase and decrease because of Black
  Friday, Christmas and all the rest of it. And then I''ll say, do a report. Write
  the email to the client, write me a team''s message to the client, formatted nicely
  and then affect the change. So I was prompted by Mike saying about hooks, actually
  putting a hook into it. So whenever this happens, always do this. So I''m thinking,
  okay, what I actually want to do is when I make a change, And to get it ready to
  send through to Google. I want. It to back it up. Back up the existing position
  for whatever it''s looking at. Do a validation of the data that''s going in prior
  to it going in. Make a run, a dry run, make sure it works, then do the live run.
  And then verify that what you asked it to do. Has, but then always have a restore
  position. It didn''t actually work the other day, the restore, but that''s a different
  story. So I was doing that as a hook. I think every time you try and change from
  Google Ads, do this process, it doesn''t actually work. It won''t do it on an API,
  a hook. But now I''ve built it into my context. MD that this is a protocol, a mandatory
  protocol at the top. Do this, this and this. It''s brilliant. Eden''s the point
  where if you''re in this super duper mode where it''s just blasting through, it
  would stop and say, I''m going to do this now. Are you all right with this type?
  Yes. To continue. So you can read what it''s saying. Type. Yes. And then it will
  go and do it. That was a belt of that. That was. I really like that one. But I''m
  doing more and more of that writing stuff back into Google Ads, which is quite scary.
  And I just tend to. Download into Google Ads Editor, do the change. And then download
  to Google Ads editor where all green bits highlights are and just see what I mean.
  Change the right thing. I said it''s caught it a couple of times, but it''s not
  done what it''s supposed to do. But a lot of the time it doesn''t re enquire on
  the Google Ads data through the API. You got to really tell it that I want the latest
  data. And then it will tootle off and do it. So I''ll go on. Your turn.'
- 'Them: Yeah, yeah. I''ve been thinking about things like that, but it''s like, I
  don''t know if. I don''t know if it''s the way I work or is the type of clients
  I got. Maybe I''m lazy. I don''t find very often that I have to do. That much work
  on the Google Ads account. So it''s more about you set up a new campaign, I mean.
  Just to get stuff, just to say in terms of search campaigns really is just. Outside
  from brand campaigns. It''s only two clients where you really use search. The rest
  is mostly shopping. Or is it mostly is pretty much all shopping op Max. And then
  we have a marketing mags. Do we need by hand? It just feels right and I wouldn''t
  be optimizing it. So. What sort of so are you talking about? Maybe, I don''t know,
  your hotels client when you have to create many campaigns and I don''t know.'
- 'Me: No, not necessarily that. One of my favorite ones at the moment. It''s very
  nearly finished now. This was prompted by a client who''s changed all his text outside
  my control. Changed all the text in his ads, but Black Friday all over it. All over
  it. Now he wants to revert it back to Christmas, and then he wants to revert it.
  To. So I said, well, you do that. You change the text. There you go. There''s the
  spreadsheet, a G sheet. With your latest position, with your headlines in your descriptions.
  You can go in and change that, and I''ll suck that in. And that''s pmax and rsas.'
- 'Them: Okay, so that''s you telling Claude, go and take this.'
- 'Me: No telling the client, I''m saying. So I''ve pulled in the latest position
  as though you were going to do it in Google Ads Editor. But all it says in the sheet
  is the text assets.'
- 'Them: How the height.'
- 'Me: I''ve actually looked to do image assets now as well, so you can change those.
  They''re a bit tricky because their IDS. But download it into a G sheet. So you
  got one sheet for pmax, one sheet for rsas. He''s landed me in the ship because
  he just got rid of who was effectively my boss. I''ve never had a boss for many
  years, but she said she was my boss anyway. So he said, I''ll help you out with
  the text. I''ll do it. Right, fine. There it is. There''s the sheet. You tell me
  when you finish, and I''ll suck that back into Google Ads. It''s been a bitch to
  do. But off the back of that. I''ve got something that will pull in. Apmax campaign.
  The asset text from a PMAX campaign. So headlines, descriptions, long headlines.
  It will pull it in. It will tell me how they''ve performed over the last 90 days.
  So really click through rate and conversion rate. I''m more interested in click
  through rate than anything else. Then categorize them. Which ones need changing,
  which ones have gone stale or just aren''t working? So it will look at it. As a
  client base, not just saying, is it less than 5? So look at that asset group. Highest
  is this lowest is that. Which one should I actually be looking at? It''ll bring
  them back in a list. I just want the high, the high priority ones. So the ones with
  the very low CTR, and it''ll tell me what the CTRs, what the conversion rate, what
  is the conversion? It will tell me why it says it''s a high. It''ll tell me what
  the current text was, and then it has a cell. With a drop down List of 15 alternatives
  of text that I got clawed to do based upon criteria that I''ve set for all the clients.
  So it''ll go and look at them, it''ll look at the URL. And it will bring me back
  a selection of different ones. So ones that are technical brands, quirky CTAs. Give
  me a choice of those. They all keep. Then I can send it back again and it replaces
  those. Assets. So it''s an optimization thing, and it''s something that. To do that
  manually. Once I get it right. It''s nearly there. To do that manually would take
  a long time. It''s something I never do. I never, ever do that. I never go and optimize
  my asset text. And you look at it, it''s lying you through. Top 1. Top ctr 8%. Lowest
  0.4. Why would you want to keep that one? What a difference that will make.'
- "Them: Well. Okay. My view probably not a lot. Sorry. I'm saying this because I\
  \ go through these reports quite often and what I see is that for big enough accounts,\
  \ and that's different story when you're spending \xA320 a day and we're gonna have\
  \ the data and there will be wastage there. But for, you know, big enough accounts,\
  \ you can see the best performing ones, the best performing headlines based on descriptions,\
  \ the ones that perform, that tend to get the most impressions. But no, you're right.\
  \ I mean, there is that. And there is also the fact that you have maybe 50% of the\
  \ headlines that are underperforming. And still spending, you know, some amount.\
  \ So it's the case of why keeping them there. If you remove them, yeah, it's gonna\
  \ be small impact, but that's the saving. And maybe that stops you from trying new\
  \ headlines. So there is some truth in that. But. Yeah, I mean, I always think.\
  \ The lazy me always think. Look, is it worth the effort if it's gonna move the\
  \ needle in a meaningful way? And maybe just ask me. You know, just. Okay, that's\
  \ an excuse."
- 'Me: You fit the nail on the head. So if you''ve hit the nail on the head there,
  because you asked the question before, why do it in Claude? Why change it in Claude?
  And the reason is I''ve got an experiment system that is logging when they go in.
  Is creating a task for me to go and looking back in four weeks time to see whether
  they worked or not. I will know categorically. Whether that has worked. And that''s
  why I''m doing things through Claude. Because I''m logging things. I know we can
  go into change history, but there''s certain things not done in change history.
  And in change history, you can''t say why you''re doing this. So the experiment
  system I''ve got is it says this is the expectation that you''ve got. Let''s go
  back, let''s set a task, because I''ve now got a task manager system as well. And
  prioritizing tasks. And it will pop that up as a priority, so you need to go and
  test this. And the task manager. When it sets the task, it''ll put in it in a great
  big chunk. This is why you''re doing it and this is what you''ve got to ask. So
  I go right. Add a note to the task. Save it, put it into Claude and says, process
  my notes. And he would have dragged all of that into Claude. And he''ll say, right
  now, go and run this. And it will go and process that task. And do the things I
  want so I don''t have to remember it. And there''s little, tiny little things. That
  I''ve changed. It''s working. Is this not working? And you look at it go, no, categorically
  that''s worked, or categorically, that hasn''t worked, and you may not have come
  to the same conclusion. If you''ve done it manually because it has got all the facts.
  Not necessarily a snapshot, but you can go back on the API and see what the position
  was before and look at it now and go, there you go. I think this. What do you think?
  Now? 50. 50. I''ll say. No, I think that''s bullshit because you''ve not done this.
  You''ve not done this. But a lot of times you go, oh, that is very good. And it''s
  because you have logged it. In clothes. I''d love to do everything in Claude, I''d
  look to not touch the dashboard at all the Google Ads, ui. But that''s never going
  to happen for a long time. But it''s been really handy. Really handy.'
- 'Them: I''m not going that deep into Google Ads at all. At all. I''ve been. Distracted
  about when you mention a dashboard you transportation list. I go down that route
  as well. So I would say probably a lot of my time with Claude.'
- 'Me: Great.'
- 'Them: Has been a lot, not everything. But what has been on productivity. So, for
  example, to have few things that build. So in terms of Google Ads, a couple of things
  I got, I''ve got, I''ve created what I call a live audit skill, which I don''t know
  if I was, I don''t, I don''t know if I use one of mics as a does not as a draft,
  as a template.'
- 'Me: Okay?'
- 'Them: And I think I created one from scratch. It has been very helpful because
  I had a couple of audits reviews for potential new clients. So look.'
- 'Me: He has a no.'
- 'Them: I''m able to do in 30 minutes. The other day. I just had a presentation this
  morning. Got a potential new client. Not, not. Not particularly interested in this
  one. But point is, I did in an hour what normally what it would have taken me otherwise,
  six, seven hours.'
- 'Me: Fantastic. We talked about that, didn''t he? That is brilliant. Absolutely
  brilliant.'
- 'Them: Six, seven hours. Yeah, yeah. That was the first attempt. I was building
  it and going through, so now I''ve had it. Next time it''s going to be a lot easier,
  not faster.'
- 'Me: Did you feed in your existing audits to that, then?'
- 'Them: Second. No.'
- 'Me: Did you feed? No. Okay.'
- 'Them: Yes. And now? Well, obviously, I. My promise included all the things, all
  the questions, all the knowledge. But no, I did not.'
- 'Me: See, that would have been my starting point, I think. No criticism. It''s just
  another way of thinking. But I would have fed in all the audits you''ve ever done.
  And say I''d want to create. Go into plan mode and say I want to produce a system
  that produces what it''s like this. Off it goes.'
- 'Them: Okay? Maybe.'
- 'Me: Have you used Ultrathink yet?'
- 'Them: Ult I think.'
- 'Me: Ultrathink. Ultra. It''s fun because it does it in a rainbow color. When you
  type in Ultrathink, it comes up with rainbow colors for the latter. So it''s worth
  just to do that.'
- 'Them: Is that? Is that. I would say that is that. Is that a cursor in cursor is
  saying.'
- 'Me: Yes. Yeah. Yeah, yeah. If you''re running Claude in cursor, in terminal. If
  you''re right, ultrathinky. Or write it. Alternating colors and letters.'
- 'Them: So if I. Let me share my screen.'
- 'Me: Yeah. Sure.'
- 'Them: Sorry. I''m trying to find. Okay. Yeah. Here you go.'
- 'Me: If you try Whisper flow out yet.'
- 'Them: Yeah, I''m wasting all the time. Make fan. I''m getting used to it. Not in
  paid mode yet, but I may. Well, I think I will agree soon. And what? What do you
  want? To show you. Okay, fine. So we are. Sorry. So is that. Did you say ultra?
  What is it? Is that. Is that.'
- 'Me: Ultra. Think.'
- 'Them: Is that here? Where would I find it?'
- 'Me: I can''t see screen.'
- 'Them: How you. Oh, sorry. Why not? You cannot see it. I''m not sharing anything
  now.'
- 'Me: No. No.'
- 'Them: Okay, let''s try again. Now.'
- 'Me: Yeah.'
- 'Them: Yeah, okay. So what is it?'
- 'Me: Just type in ultra thing there.'
- 'Them: Ultra thing.'
- 'Me: Yeah. No gap, no space. Right. It must be in Terminal then. Can you go into
  Terminal? Is it Command T or something? That''s it. So if you go into Claude there.'
- 'Them: This is what you mean.'
- 'Me: Yep.'
- 'Them: Okay. This is how you''re using it.'
- 'Me: That''s how I use it. Yeah, all time.'
- 'Them: Then. Okay?'
- 'Me: If you do one.'
- 'Them: So, you know, using this chat box.'
- 'Me: I use that all the time. I''ve got four of those going any one time. So if
  you type in if your query there. And you use the word ultrathink in there. Just
  type ultrathink. Now, that''s the fun bit to start off with. There you go.'
- 'Them: So is that it?'
- 'Me: But it''s really handy because, you know, you could use. You could use Opus
  Force on it, whatever it might be. Using ultrapync, uses the most powerful model.
  But you can do it per queries. You''re not paying a huge amount of money for it.
  So if you. If you would. If you wanted to do some analysis, say you wanted to do
  analyzed Black Friday results for such and such clients. Comparing with last year.
  Ultrathink. It will take longer to do. It''ll do a deeper thinking. Most of my stuff
  I use Haku. I''ve got it to default. All the agents and launch. Most of the agents
  and launch agents use Haku rather than sonnet or Opus 4.5. Because they''re more
  expensive. I know he dropped down every now and again or go up to this. That''s
  a great way to do it.'
- 'Them: So you go. You go ultra think and then you type. Then you press enter, I
  guess.'
- 'Me: No, no, no. You just. You just use the word ultra in your.'
- 'Them: The question.'
- 'Me: Prompt.'
- 'Them: Analyze. Analyze search. Intent for client? I don''t know. Campaigns for
  the past 30 days.'
- 'Me: Yep.'
- 'Them: Is that what? You okay? Fine.'
- 'Me: So just. It will take longer to do it.'
- 'Them: Okay? So tell me, tell me again. Why is this better than just going through
  this box? And just, like, asking the same question.'
- 'Me: You know what? I don''t know. I just prefer it.'
- 'Them: Okay, fine. Okay.'
- 'Me: I think part of it is because I''m from a Unix background. And I just get really
  excited seeing UNIX commands. I''m doing IT backup and it says tar. And he''s going,
  bloody hell, tape archive fantastic. I''m old enough to know what it means. It''s
  like grep grab expression. Orc.'
- 'Them: The type one is not very. I find it not very responsive. I don''t know. But.
  No, I mean, you''re familiar with it, that. That''s where you.'
- 'Me: Well, let me share my screen with you. I think it''s fun to see the way other
  people work, isn''t it? Because we''re giving so many different ways to do it.'
- 'Them: Oh, wow. I mean. This. Oh, my God. Oh, my God.'
- 'Me: That''s the way I work. And it''s like, as you say, I''ve got this. Oh, he''s
  still waiting. There, let''s hit yes on there.'
- 'Them: And of course, of course, this is just one of screen.'
- 'Me: Yeah. Well, this is the three sessions I''m doing. If I go up here and just
  split that. If I do ca. I''ve got an abbreviation for this. It''s got bypass permissions
  on now. The bottom there. You see that?'
- 'Them: Yeah, yeah, yeah.'
- 'Me: So that''s the bit where it doesn''t ask. Like I''ve got that middle one said
  yes or no. Sometimes I might want to look at other times I just want to blast it
  through. I don''t want to be interested. But if I do shift and tab on this one now,
  I can still go to plan mode.'
- 'Them: Yeah.'
- 'Me: So, you still there?'
- 'Them: Yeah.'
- 'Me: It''s just kicked up another screen because. I''ve lost reset. You''ve actually
  completed there, so keep that with me a minute.'
- 'Them: I''m still seeing your terminal.'
- 'Me: What on earth this happened? There. I''ve just lost the. There we go. Does
  cut it. What was I saying then? Yeah, I can still scroll through these so I can
  go into plan mode if I wanted to. Shift and tab bypass Shift and tab. Don''t know
  what that one is, but then accept edit on. So if you start it with this flag, you
  can still flip between all the others. If you wanted to step through it a bit more,
  you can still use that. Accept add its own. Or if you wanted to do something quick,
  you can just do bypass permissions on.'
- 'Them: Yeah. Yeah, okay.'
- 'Me: I do find that really interesting.'
- 'Them: Yeah, indeed. I mean, you have tasks going on for hours.'
- 'Me: But that''s what happened with the. With the. Doing the. The knowledge base
  one, because it then went off. It found a whole new load of articles to go and do.
  Had to do a web pool for all them. Sorry, a web fetch. And then stick them all into
  the database, and then. So I''m just leaving that running. Another really interesting
  one is doing unit tests. That''s one of mics that where you. You say to it run or,
  or you can do some setup. Unit test or run unit test. Specify unit tests. And the
  unit tests go into your code. And test it all. And it will toot laugh. This stuff
  it found I was getting dead locking. I was getting old scopes were wrong. It was.
  It saved me so much time just using unit tests. And it will just. I say one of these.
  It''ll just run through. It''ll just keep running through. And said, so many passed.
  I''ll do them in phases. I think these are important. These are important. These
  are important. It''ll run them and then carry on.'
- 'Them: So you need. You need tests. Okay, unit test.'
- 'Me: Your project.'
- 'Them: Your project, your. Your agents as well, I suppose.'
- 'Me: Everything? Yeah, everything. Yeah.'
- 'Them: Okay? Because you have staff running all the time, right?'
- 'Me: I''ve launch agents running. Yeah. And they. I''ve got an agent dashboard now.
  I got to keep my eye on them because every now and again they''ll just bomb out.
  And I''ve got one thing I found was because I''m switching my computer off every
  night, so if I set a schedule, They weren''t running, I''d set them for 6:00 in
  the morning, start at 7. So now there''s that flag that says, if they''ve not run
  already, then run them. And now I''ve got another thing that runs. I''ve got a health,
  a slash command. So I''ve got health and it''ll run that command, that skill. And
  it''ll just. It''ll blast it through. Make sure everything''s working. I''ve got
  launch agency. It''ll just go and start everything.'
- 'Them: Yeah.'
- 'Me: Seriously, all this stuff about the electricity and cloud servers and AI taking
  all loads and loads of electricity, it''s me. It really is me. I''m just totally
  addicted to this thing. I think it''s fabulous. And this, you know, the most important
  thing. There''s stuff I''m producing for my client is extraordinary. I did. I did
  a landing page report for a client the other day, and it happened to have failed
  the landing page report, and it was like that. And I put screenshots in of the landing
  page before and after and what I was testing and why it had failed and why I thought
  what we could do in the future. And she just put one sentence in. How does the landing
  page test going? And I set this thing back and I went, christ, that is my. Fee for
  a month doing that, to actually produce that in that level of detail. Would have
  taken me a day at least, and I just rattled it off in maybe an hour because I wanted
  to really over ag it.'
- 'Them: So let me go through that. So there is a landing page test, which I assume
  means that the client created a secondary landing page.'
- 'Me: Correct.'
- 'Them: And I don''t know, maybe you have a campaign. 50% traffic going to one page,
  50 or the other.'
- 'Me: It''s an experiment. It''s an experiment on Google Ads. Experiment.'
- 'Them: And he asked you, well, how is the experiment going? Fine. And you go and
  tell Claude the client is asking me this.'
- 'Me: Yeah.'
- 'Them: Based on the context information and.'
- 'Me: No, I didn''t do that. No, I didn''t do that. I said email sync. It ran the
  email sync. It''s labeled the emails for clients. I said, read Helen''s latest email
  and comment on it.'
- 'Them: Okay, I comment on it. And then you get the response what it does. What?'
- 'Me: Well, it produced a report or only page report? I had to do the screenshots
  of the so desktop and mobile for both of them. I said, drop this in there.'
- 'Them: It was a critique on the landing page or it was just data.'
- 'Me: Is it? No, it''s a test. So I. I sorry, it was. I didn''t explain that very
  well. It was an experiment in. In Google Ads for an ad variation. They had variation
  was landing on different pages. So it was a. It was a landing page test as such.
  But the data was in. In Google sending it half and half.'
- 'Them: Yeah.'
- 'Me: So that.'
- 'Them: So it got the data from the variant test and it just produced a report on
  that data. So you come and look. I don''t know. I mean. What? What? I was just wondering.
  I mean, that is so. If it''s landing page, it''s more about conversion rates.'
- 'Me: Yep.'
- 'Them: It''s more about cost per conversion and things like that.'
- 'Me: Yep.'
- 'Them: But you talk about screenshots, so what was that?'
- 'Me: But the screenshots were the actual landing pages themselves. Where it was
  sending it to, so did desktop and a mobile version. And I asked it to critique the
  landing pages as well.'
- 'Them: The landing page critique is it was the real valuable thing from.'
- 'Me: It was. But we''d done another test earlier, another month. It was about that
  big of a review on that one, because I''d done it myself, and it was. It was quite
  favorable, this one. There was no conversions at all in the period for either of
  the variations. They''re usually quite low anyway, and he told me why.'
- 'Them: Okay?'
- 'Me: It actually explained why.'
- 'Them: So you have. Sorry, keep interrupting. So you got your. I don''t know, maybe
  you have a skill that goes through landing page critique. Now. Okay. Just Claude
  criticized landing page.'
- 'Me: Yeah. Yeah. Yeah.'
- 'Them: Okay?'
- 'Me: And as time goes on, what I might do is build some more stuff into my knowledge
  base. So the knowledge base now is being built upon going and looking on the web.
  It''s built upon playbooks I''ve created for clients. It''s built upon pro post
  mortems of them. Provides. I''ve just done one for Black Friday for a client. You
  know, we did this, and this happens. And my own knowledge. There''s actually a section
  in the knowledge base which I''ve not run yet, which is going to be an interview
  phase where it''s going to ask me things that I do, things that I think are good,
  things that I think about.'
- 'Them: Yeah, yeah.'
- 'Me: And I said to it, that''s fine, but I don''t want this to be my opinion. I
  want this to be statistics based, say. Right. Okay, well, I''ll bear that in mind.
  So I might be saying I think we should be doing this, and it''s actually wrong.
  Statistically, it''s wrong. And I want to be pulled up on that. I don''t want it
  to be my opinion. I want to be able to give it the input. And it''s called the Rock
  Systems Methodology. So I want to give it that input, but I don''t want that to
  be the. The total driving thing, because if it''s wrong from the start, it''s going
  to be wrong for everybody then. So that''s why the knowledge base for me is the
  most important thing that is my brain.'
- 'Them: Yeah, yeah.'
- 'Me: The rest is access to to to Google Woocommerce. Got a woocommerce mcp server.
  I''ve got a shopify mcp server. That was relatively straight. It''s a bit more complicated
  than the WooCommerce one because you got to create an app within Shopify. But now
  I can interrogate Shopify directly. Google Trends is a real shit. Don''t bother
  with MCP for just awful keeps timing out, it just doesn''t. Like it doesn''t. It
  doesn''t like too many API calls in one going. Google Trends does tend to use a
  lot. I won''t. I won''t bother with that analytics.'
- 'Them: So shopify mcp and I. I don''t have any shopify integration. I''m not going
  down the mcp road. What I do is I. I have an API libraries that the way that they.
  That the road Cloud took, which is fine with me. And. And one talks about mcp servers.
  And I feel like I''m missing out on it, but it''s just, you know.'
- 'Me: I don''t know. Seriously, I don''t know.'
- 'Them: Yeah.'
- 'Me: Sometimes you say, go and interrogate it and it''ll go. I''ll use the mcp.
  Oh, that''s no word. I use an API direct API call.'
- 'Them: Okay, sorry.'
- 'Me: So I suppose I''m giving it an option. I just thought mcp servers. The right
  way to do it. Going back to go marble because they use MCP servers.'
- 'Them: Yeah. That''s why I I By the way, I I remember Marvel, there''s so much going
  on and too many ten pounds here. I mean, in terms of AI anyway, so this Shopify
  could be very interesting as well. I think. Yeah. Because, I mean, in terms of,
  obviously, sales. Product performance, product stock. And. And things like. Yeah,
  I mean, margins as well. And. What? I wonder if that''s something I use. I have.
  I have my. My Shopify. App, which I use, but it''s not linked to clothes, it''s
  linked to my scripts. And I keep. I have a number of reports taking data which I
  daily but that''s not been integrated into Claude onto the grain. Like it could
  well be, anyway. Yeah, I''ve been working on something like that. So, as I was saying.'
- 'Me: I know you can do this yourself, but I can send you the process for Shopify.
  I just drop it down and email it here? Want to pull that straight into Claude and
  say, I want to do it for that client.'
- 'Them: Yeah.'
- 'Me: Because it works.'
- 'Them: Yeah. How do you. How do you use the Shopify data? What do you get permission
  to provide? Is there a stock, for example, gives me the best sellers or. Or what
  products I should. I don''t know in terms of a stock, what products I should stop
  advertising because of lowest stock or what.'
- 'Me: I''ve not scratched the surface. The only thing I''ve used it for, to start
  off with is I wanted to find out an overall roas for the clients.'
- 'Them: Is.'
- 'Me: Because they don''t do much marketing elsewhere. So I tend to quote the Shopify
  figure. As the revenue and Google Ads is the cost.'
- 'Them: Yeah.'
- 'Me: So I don''t know. The main thing for it. You got to jump through a few hoops.
  On Shopify to set up the API bit, and that was the pissy bit.'
- 'Them: I''ve got that already, so that''s. But, yeah, I mean, that. That''s. That.
  That''s exactly how I use it. So I get the client asking me, overall, I need the
  rows of six.'
- 'Me: Okay? Yeah.'
- 'Them: Upon. I have this in my dashboard, which sits outside cloud, anyway. It''s
  monitoring that daily and that''s. That''s how it works. But it would be cool to
  have. But anyway, it''s not integrated because I. I still want Anyway, it is not
  part of my. But in a way, in terms of what else I''ve been building, I mean, one
  thing I so there is that. There''s this. I was. I was saying about the light review,
  which saved me a few hours, and actually, it found a couple of things I would have
  missed. But you''re right. I didn''t see that. I didn''t. I will do probably will
  do that. Those, those audit reviews I like the most that will fit them into the
  quote and see how we improve. I mean, that''s probably going to be what is the light
  review and more the high level, not high level, actually. The detailed review, the
  deep, the real. That''s probably what I can do to fit, because I still want a different
  audit review levels.'
- 'Me: Yeah. Yeah, yeah. And that''s your. That''s your value that you''re putting
  into it. You know, to. Then you''re going to get the reviews out in the style that
  you want them, and that is you. That''s what you know, that''s that. ''s the bit
  you add to all that.'
- 'Them: Yeah, indeed. Indeed. Yes, yes. And the formatting as well. So half a half
  scale and that. So basically, I have these calls and sometimes I don''t necessarily
  prepare many of the calls because I speak into my clients and I''ve not done four
  years, so I really know everybody. But for some, for some others, you need to prepare
  those calls. So I have a skill that does that. So I just, you know, prepare. Prepare
  my agenda or my meeting prep, My meeting prep document. I think that that is an
  issue that was initially based on one of Mike''s skills, but back on my call with
  clientex tomorrow morning,'
- 'Me: Yeah. Yes.'
- 'Them: And he just asked that. And he gets everything into a slide, a Google Slide
  with the right formatting, the kind of log, everything. So preparing something like
  this. Okay, I''ll use it twice, so we''ll see.'
- 'Me: I look at you, I love it. You can''t stop smiling about this as well. It''s
  brilliant. Because that''s exactly how I feel. Because you, inside your head, you
  go, wow, that''s amazing.'
- 'Them: Yeah. Because. I probably wouldn''t have done that, but if I had to do that,
  he would have taken me two, three hours now.'
- 'Me: Yeah.'
- 'Them: He took me to the hours to get the whole thing done. But the following call,
  it took me 10 minutes. And it took me 10 minutes. So I prompted waited three minutes.
  Get these light show already. The formatting, the words, the titles, the log, all
  the dates, all sorted. It took me 10 minutes to refine because it''s never. I mean,
  it would never be Find some of redundant stuff.'
- 'Me: Correct.'
- 'Them: But it was really good because obviously went through all my slack. It''s
  like channel communications work through my emails, my nutri notes. So it came up
  with a couple of things. Oh, I had totally forgotten about this. Oh, that''s my
  point. And to be honest, there''s not so much AI in that.'
- 'Me: Awesome.'
- 'Them: The AI is summarizing all the communications and so on them into a cache
  and then getting everything into this slideshow or the document, the Google Slide.
  It wasn''t AI, really. It was just the app.'
- 'Me: Yeah.'
- 'Them: It was just taking the formatting, so it was not. Claude. Create a Google
  sheet from scratch with the client. Logan. And no, this is the template. This is
  the cache with all the data. It''s already summarized.'
- 'Me: Yeah.'
- 'Them: Now. Am I lying? No, I think I had much to do with that. And some of the
  things I built is reminder. So I''m not using agents yet, but I have jobs that run
  all the time. Or every couple of hours. So there''s one job that checks my slack
  communications, my emails and meeting notes every couple of hours.'
- 'Me: Yep.'
- 'Them: Ten me as lack notifications for any tasks or reminders. So there is this
  email from this client. These are the three reminders. And it adds that into my
  dashboard, which is a task management tool I just built as well as you did. It just
  has actually four reminders and it goes hard to approve them or not approve them,
  accept them, or they delete them. And that''s automatically just fits.'
- 'Me: Yep.'
- 'Them: So it''s really useful for notes, for meeting notes, because Granola. So
  I have a call. Hang up, forget about it. And with the next hour, I will get reminded.
  These are the actions that go from Granola to growth into slack and from slack.'
- 'Me: Yeah.'
- 'Them: Well. And then into the dashboard. Into my dashboard. And, yeah, I''ve got
  that. And I cannot forget, really, and I kind of. Kind of focus on the next goal.
  And then after, you know, just go. Okay, These are my notes, are the actions. Fine.
  This is an actual task. This is just remembering. Oh, this is rubbish. I delete
  that.'
- 'Me: I like the reminders thing. I think that''s to. To add that on because there''s
  a difference between tasks and reminders, isn''t.'
- 'Them: Yeah, let me show you. Because we keep showing me all the time.'
- 'Me: There.'
- 'Them: I want to. I want to show up. I want to show off a bit, if I can. Let me
  see this response because I haven''t serviced down, okay? Let me get rid of the
  Ultra thing.'
- 'Me: I think this is one of the things that I''m finding is I wouldn''t. I couldn''t
  sell this. At the moment, it''s far too flaky to sell, you know. I mean, the number
  of errors it makes is quite extraordinary, especially on data. You''ve got to really
  watch it, you know, because. Oh, I didn''t know you meant that. I''d just be working
  this for two fucking hours. What do you think I meant? I actually scroll down here
  as well, and it swears back at you when you. When you say to you really fucked up,
  that, yes, I really fucked up there.'
- 'Them: Yeah, well, yeah.'
- 'Me: Well. I ran. I ran one of Mike''s skills and that said bollocks in it. I think.
  You know, that''s Mike. That is. That really is. A nice one is slash client. Where
  you. If you''re. If you move between clients, you kick up a new terminal and just
  do slash clients and then the name of the client and it loads the client up for
  you, so there''s no ambiguity about what you''re working on.'
- 'Them: Oh, yeah, I see. Yeah. Let me show you just to show up a bit. I know as impressive
  yours. But these dashboards and this Diabo just goes through all. But then I can
  select all the clients. These are Clients are really so I have. I don''t know. So
  Shad. That''s why I have reminders and tasks.'
- 'Me: Brilliant.'
- 'Them: So this task is in sync with my Google Sheet task, which I share with the
  client.'
- 'Me: Okay? Yeah.'
- 'Them: Because the client is checks in I don''t know. So 8 inch they make I sync
  that with the Google sheet and the Google actually that can open and change and
  this this section here, this graph hub is thinking the starts with what I call in
  the.'
- 'Me: Yeah.'
- 'Them: In the Google sheet and these are reminders. And this is what is being fed
  from meeting notes from an emails. So I get, so I don''t know, I got an email. I
  don''t know if I have any. That need to approve. I may not have any to approve,
  but it basically will tell me. Look, this is a reminder, so I need to perform this
  client.'
- 'Me: Yep.'
- 'Them: I need to repair the plan for February March testing period. These are some
  nodes taken from my call yesterday. Some of them are duplicated. Maybe, but anyway
  gives me an idea and have the tasks. Fit as well, and I can go and obviously make
  timeline. And. And. And they have even had templates. Okay. I need to prepare a
  reminder kind of a task. For promos. So give me. So just give me all the steps.
  I just add the name, the date. Fine. Create workflow.'
- 'Me: Oh, I love that.'
- 'Them: I don''t know. Window sale, for example. 20, 25, I guess. I don''t know.
  With the sale. Gentle sales. So say, okay, fine. This is going to launch on, I don''t
  know, it''s going to be on the time unboxing day. Fine. So clear the workflow, and
  then based on that, I have this. Check the dates. Okay, fine. This is actually going
  to be, by the way, give me approximate dates and then. Label, and then I kind of
  blow for high DP because some of these steps will develop for some Granola. Anyway,
  it''s just me having fun. Do I need this now? Make my life easier?'
- 'Me: Brilliant.'
- 'Them: Yes. Was it fun?'
- 'Me: Yeah. Yeah, I feel that matters, isn''t it?'
- 'Them: A lot, you know? Daily briefs so I can send okay I missed nearly forgiven
  because my PC was switched off so I sent daily brief and it would tell me the meeting
  the clay might things have a day priorities reminders available for the day and
  for the week or prioritizing a really nice way as a slack message because I''M trying
  to get everything into slack.'
- 'Me: Yeah. I think, yeah, it''s having that single point of communication beyond
  email, because I''ve got WhatsApp and I''ve got teams.'
- 'Them: Yeah.'
- 'Me: The only way I can do that is literally to select all and paste it.'
- 'Them: Yeah.'
- 'Me: That''s the only way I can get it in. And it is so annoying. If the client
  doesn''t use slack, I don''t know how I can force them to do it.'
- 'Them: Yeah. Had a client who. Anyway, yes, you''re right. I have also some dashboards.
  Have a health dashboard.'
- 'Me: Okay?'
- 'Them: Which, okay. Well, sorry, I don''t know. It''s not working now. How to use
  it for a few days. This is basically telling the state of the caches, the email
  cache and so on.'
- 'Me: Right. Yeah.'
- 'Them: And then I''m working on. Okay. I haven''t used it for the. I was working
  on engaged engagement score. So the idea is, look, there''s some clients who are.
  You know, I just forget about them because.'
- 'Me: You''re right. Yeah. You''re right. Yeah. It''s a great one.'
- 'Them: This is kind of a score, a dashboard that will tell me, look, this client,
  I don''t know, this is gold, silver, bronze. I have to reach 60 points every week
  and 60 points if I have a call. That''s 30 points every email. I said every Slack.
  Let''s check. SM is 5 points if I unless there could be some. It counts the number
  of changes in the Google Ads. So if I make every. Every change in Google Ads I make
  is 3 points, and it just scores every week and I reach it and it''s. It''s kind
  of gamifying just to make.'
- 'Me: You''ve done nothing. On it. Yeah. Yeah, that''s very good. And do you. Do
  you feed into that how much they''re paying?'
- 'Them: Sure.'
- 'Me: As a proportion of how much money you''re right.'
- 'Them: Yes, yes.'
- 'Me: To keep it, isn''t it?'
- 'Them: I think. Well, yes and no. That was one of the inputs. But I feel uncomfortable
  about that because I don''t know. How things will evolve. So I just say it''s high,
  low, medium priority, but essentially the same but. Yeah, and there''s some but
  in terms of demand as well. So this is a very demanding client. So the 60 point
  goal level for some. For some is 60. For some it''s 80 or 90, depending on how much
  they pay, how demanding they are. Because some guy is, you know, they''re just happy
  to get a monthly update, and that''s about it.'
- 'Me: Yeah, yeah.'
- 'Them: The weekly call. Some others will have checking badges weekly. So I''m still
  building it, but the idea is, look, I just go in and say, okay, every. You know,
  these are in good shape. I didn''t speak into them. I think hundred calls with them,
  communicating with them, doing, doing work on Google Ads at this point is just number
  of changes. I don''t know. It could be hitting weekly budgets and so on. And it
  tells me, look, these are in the red zone because you haven''t spoken to them in
  all week. You get it?'
- 'Me: Yeah. It''s. It''s almost like you''re saying if you went on the phone call
  with a client now, how embarrassed would you be? You know?'
- 'Them: Well, only get there, probably, you know, find my way around it.'
- 'Me: Yeah. Yeah.'
- 'Them: I suppose so. I. I would say no, but that''s probably going to be a lot of
  some of that. But, yeah, there is some of that sometimes. But. But yeah, that''s
  about it. It''s kind of making it fun. So it''s more finding, finding the incentive
  to go into that account. No one cares about, not even themselves. Because I thought
  some of the accounts I enjoy the most is those clients are really active. You know,
  they email me. They''re not demanding, but they are people and generally interested
  to making things work.'
- 'Me: Yeah. Yeah.'
- 'Them: For them and for me and for the business. So, okay. Can we do this? I''m
  trying this and that, but some others, you ask them something. Oh, yeah, fine. And
  then nothing. For. For days, for weeks, you can be reminding them nothing. So those.
  I tend to neglect them. You know, they. They pay. They don''t complain. Well, don''t
  complain that you go to a call and they. Anyway, it doesn''t matter. So, yeah, it''s
  kind of making it fun to me to find other reason to go into that and work for them,
  because otherwise. Just forget about them.'
- 'Me: Y. Eah. Yes. Yeah. You do? Yeah. No, I think that''s brilliant. I. I have a.
  I have a client. It''s slightly off topic, but they do a kids toy. I think I''ve
  spoken to you about them before. And I, he. He''s been. We''ve been. I''ve been
  working out strategy to increase budgets and change target roas and so on. And over
  Christmas, it just goes nuts. And they always run out of stock because it just gets
  out of hand. I know. I looked at it the other day and you know when you just look
  at numbers and you don''t really go, Yeah, I''m not looking at that as actual pounds.
  I''m just looking at that as a number. And I''ve got to increase, decrease, whatever.
  And I looked at it the other day. Because I wanted one of these toys for my nieces.
  Son. So I emailed him and I said, it is the only chance, you know, you. You could
  do me a deal on one of these. And I looked at what his Q4 sales were in the US since
  October. It was $9 million. And I looked at how much I charge him. And what and
  when. If he doesn''t give me this for nothing, I''m going to go absolutely nuts.
  Thankfully, he emailed back very, very quick. Oh, yes, you can have whatever color
  you like. You know, I get it straight away, blah, blah. And I''m looking and going,
  yeah, you will, won''t you? But it was funny how it''s like that engagement thing.
  For the rest of the year, I won''t hear from him. And then the Q4. That''s when
  it''s all going to go absolutely nuts. But all that preparation for. For the rest
  of the year has produced those figures now. So it''s one of the best success stories,
  that. But actually doing budget changes because one minute he''ll say, I we''re
  running out of stock. Slow it down. Next minute I say, we found some stocks, so
  can you increase it? And I''m just going in and just saying, saying, read the email.
  Come up with an email back to him. It''s about an A4 page long. This email. Send
  it off to him. The action, the changes and documents it. So send another email,
  say, I''ve just done this. And that''s one of the nicest because I, I, it''s funny
  looking at your, your dashboard, I look at it go, that looks really polished. That,
  that''s a really nice way to do it. I''ve been more textual based than anything
  else. I''m working in within the system, within Cursor rather than building metas.
  Manager is outside Cursor. I put it onto a browser, but everything else has been
  text based. And I''m just running it straight from text. Eventually I''m going to
  have enough stuff in there to be able to go, okay. Let''s gather all this information
  together. And do a planning session one day to say, let''s try and create a dashboard
  that grabs all this stuff together, and it makes sure I have a universal approach.
  It''s only been recently I''ve said I''ve realized that the skills I''m creating
  weren''t universal skills. I''ve been working on a client and saying I want to do
  this. And they say, right, well, I''ve done that. Then go to another client and
  say, right, can you do this? Why? I don''t have that skill. And you go, oh, Christ,
  no. It''s not actually universal skill I''ve created. So. Okay. We''ll go and look
  in. Go and look in such and such. About this. The skill in there or it''ll go and
  find it. He said there''s a skill in such and such a client. Do you want me to use
  that one? Well, yeah, I do, but I also want it to be universal skill. And it was
  that structuring of the directory. That you look at you looking at that on a regular
  basis and going, hang on, he''s not writing. And like doing tidy ups. All like the
  tasks I don''t use. I use Google Tasks very infrequently now. Mainly it''s just
  the system task list that I use, but it was saving them in different places. It
  wasn''t saving the task. JSON in the same place all the time. So I got it to tidy
  all that up and then it the next time you go see, I can''t find the tasks. And another
  skill. Was referring somewhere else for the task. So it''s that. It''s making sure
  everything works together. It''s been quite complicated. And all it took was the
  right prompt. And you go, yeah, yeah, I can do that. Yeah, yeah, no problem. Why
  don''t you just ask me? You know? Yeah. And you think, oh, God. So then going back
  through it. So I think that''s why I like terminal, is to go back and go, well,
  why is that there? That shouldn''t be there. And then it starts to unearth other
  things, doesn''t it? So I think eventually, once Christmas is over and I''ve got
  some time, I think I would like to do some sort of dashboard and then I can say,
  well, I don''t have to go and do client, blah, blah, blah, it will just go and do
  that in the background.'
- 'Them: Yeah. Let me, because I spend days fighting for this. The reason I moved
  from having a web UI to going back into cloth was because I cannot use scales. From
  the web ui, so those skills are not available to the API. There is a cloud. I ask
  a question to Mike, which is in the, in the. In the app, in the 1820 app. Passing
  up on actually got really confused with my questions, I think. But the point is
  that I struggle with that because I was very keen on using a web ui, as I showed
  you the other day.'
- 'Me: Oh, really? Yeah. Yeah.'
- 'Them: How to abandon that, give up on that. And go back into the. Not the terminal,
  but kind of the black screen. Because I could not use the skills. And it''s fine.
  I mean, it''s no big deal. Actually, I find it fine. But that was big deal for me.'
- 'Me: Then, wouldn''t you? Rather than use the skills you''d have to build a proper
  app. Because you could use them. You could use like light railway or. Or, you know,
  a lot of it is flask cap, isn''t it?'
- 'Them: I don''t know. I mean. There was no. Okay, I''m maybe not inside your question.
  There was no way available. That I could find. I asked. I mean, I went through everything
  and I asked. God, I asked. Anyway, there was no way available it will be to invoke,
  kind of invoke the skills I had in my app.'
- 'Me: Right. Oh, I see.'
- 'Them: Through the API, because the API connects directly to, I guess, the cloud
  API. And that that didn''t make the skill available because it''s sitting in my
  app.'
- 'Me: Okay? And this is funny because we get to this sort of. This sort of stage,
  it is beyond my knowledge. Sometimes in the way it works. It''s like the Railway
  app. You''re using that very simple example of the. Of taking the picture of the.
  The. The recipe cards. I know I can''t do that on my own website, so. Got me, like,
  you''ve got the ad success one. I can''t create a subdomain on there and just run
  it on there because it needs. It needs something. It needs Python anywhere is it.
  It''s a. It''s. It''s. It''s the thing that you would put on your own app so you
  can run Python on your. On your.'
- 'Them: Some driver. I''m going to buy that anyway.'
- 'Me: But it facilitates being able to run Python scripts on there. But then you
  get into the problem of, yes, the cloud interface. You''re going to have to use
  cloud API, then. Which then starts to invoke cost, which I''ve done on some of my.
  Unbeknownst to me, I''ve. I''ve been incurring abi costs on there.'
- 'Them: When we use cloud code, we use API costs, so. So I have. Well. I have Cloud
  Max, and that''s for Cloud AI. AI. And that. That is outside the app. That. That''s.
  That''s me playing up with some other things.'
- 'Me: Yes. Y.'
- 'Them: And then we have code, and that''s linked to the Control API. And those.
  Yeah, you have to keep putting money into that.'
- 'Me: Ep. But if you''ve got Claude. If you''ve got Claude, Max.'
- 'Them: Yes.'
- 'Me: And you''re running Claude through your cursor.'
- 'Them: Yeah.'
- 'Me: You''re not using any API. There''s no additional API costs on that. That''s
  all encompassed within your Claude Max.'
- 'Them: Okay, I''m missing that.'
- 'Me: Yeah.'
- 'Them: That''s not.'
- 'Me: You have an allowance in your Claude. Max.'
- 'Them: Sorry. Let me. Let me share my screen. So I have. So. There is. This is claude.
  Okay? And I have max plan. Okay? And the campaign, whatever. And then this is one,
  and the other one I''ve got is entropic. And let us see. Because I was getting.
  Yeah. So, yeah, I have entropic API, and this is. This is what I''m using and extending.
  So I have spent two hours in the last week, so I''ve not really. But the point is,
  I''m buying credits.'
- 'Me: Yep.'
- 'Them: I mean.'
- 'Me: Yeah, I. I do as well. There''s only certain things within your brain. That
  actually uses those credits, and it is the ones that are running independently.'
- 'Them: Okay? I don''t know.'
- 'Me: If you''re running like a, a launch agent or something like that, that''s running
  without cursor, without you interacting via cursor, it will use those, those API
  calls. And this is why you need to look at your launch agent and make sure you''re
  using HeyQ, the cheap one. When you use a lot of Claude.'
- 'Them: Yeah. Yeah.'
- 'Me: If you''re using the Opus 4, Opus 4.5, it eats those quite quickly. But ask
  the question. Of claude. When do I use? When am I incorrect incurring API costs
  considering I already have a claw max and it will reveal quite a lot of things to
  you because I had this conversation with it. The other day. And it. It revealed
  a lot because it''ll say, well, this is where you''re incurring those costs. These
  are the agents they''re incurring. Do you need to use this level of Claude, Claud?
  The Claude model to do this? And some instances you can pull it back even further.
  But $2 is neither in or there is it.'
- 'Them: Yeah.'
- 'Me: That''s why it''s not going up quickly, because your Claude Max account has
  been used within. Within your cursor.'
- 'Them: Spending. I don''t know how we know how. How does it do it? Because I have
  added my entropic API. My entropy key. API key. Sorry. The topic API keys. I haven''t
  given it any clue. AI key. So how would it know that?'
- 'Me: Wasn''t there a no author similar to an oauth right at the very beginning?'
- 'Them: Yeah, but I thought. Okay, okay, it''s easy. Sometime now. So I have. And
  I''m still showing that we have this file code. This is the one I gave it. Key for
  testing. I''m not using that. But there is nothing. Include AI, which is the one
  I''m showing you now. There''s nothing.'
- 'Me: I don''t know. I. I genuinely don''t know how it connects, but it knows you''ve
  got a. A Claude Max account.'
- 'Them: Okay, fine.'
- 'Me: We must have done it at some time when we set the whole thing up. Like whether
  it. Whether. Whether it''s in. Because it''s probably in. In cursor, isn''t it?
  Within cursor. You''re telling it you''ve got an account?'
- 'Them: To be frank. Why not to be found? I''m trying all the time. I''m finding
  very frustrating. The conversations I''m having with. I mean, well, that''s not
  true because my lack of vision was useful. But anyway, I find a call is not always
  really clear about. APIs and keys while using this of that. But not. Not. But I''m
  not being. I don''t. I remember not because my Dasco. I mean, there was a time.
  There was one day when it got. Because I. I remember when it had my last. My late.
  My last call with you. I felt a bit frustrated. About how things were going. I was
  getting all these talking issues and so on. And.'
- 'Me: This terminology. A lot of it, isn''t it? A lot of it is terminology because
  it''s new terminology to us.'
- 'Them: Yeah, but there was. There was something, anyway. I. I got past that point.
  I think I. I was able to trust I understood thing about tokens, I got more relaxed
  and because I understood the context stock in his 200,000 as opposed to 12,000.'
- 'Me: Yeah. It''s so annoying when it compacts as well. That''s really, really frustrating.'
- 'Them: He was really confused the way and I was getting some Airbnb anyway. You
  know, I just got past that point. And I obviously understood. I kind of used the
  skills. Within the web ui. So I moved away from the UI and I kind of simplified
  things. I made more confident and anyway,'
- 'Me: Y. It''s a proper tool, though, isn''t it? It is a proper tool. It helps us
  with our job. I say, you couldn''t necessarily give this to someone, say, go and
  use that, then you can go and do it. It''s not like that at all, and that''s what
  I love about it. That it is. You know, you''re downloading from your head. Stuff
  like. Like the landing page. It just go go look back through my emails. I can''t
  remember when the landing page test started. Anyway went and found it. And you just
  go, God, I never remember that. You know, and it''s just joining the dots with all
  that. And, like, creating monthly reports. What have I done during the month for
  this client? I have no idea. What were the results of what I''ve done? Well, there
  you go. It''s. It just. It just does. It. It''s that completeness that. It''s really
  quite scary, but I''m. I''m. I''m absolutely. As much as your grin tells me, I''m
  really enjoying it as much as you are.'
- 'Them: So really to me when we are in a situation now do you have a hard stop now
  or you can find so I''m not going to take all the time.'
- 'Me: Yeah. No, no, no.'
- 'Them: I want to go and take a nap. I don''t recall this morning. I did a presentation,
  so I''m really tired, but anyway.'
- 'Me: I just cancel my call at 2:00 and I can''t be doing with this.'
- 'Them: No, no, no. I was looking forward to it.'
- 'Me: No, no. I just canceled my call at 2:00. Yeah, I didn''t know. I did it early
  on this morning. I just. I didn''t have the capacity today. I''ve had to take my
  sister to the hospital this morning for an appointment, and it''s just. It''s been
  full on all day. The last thing I wanted to do was speak to a client. This has been
  a good relief, I think.'
- 'Them: Okay, Fine. Sorry. Finally. Go well, we''ll catch up another time. And. And
  go into some of the things as well.'
- 'Me: Yeah, absolutely. Yeah, I''m. I''m happy to do this every week. It''s the voyage
  of discovery, and no one else understands what the hell I''m talking about.'
- 'Them: Let''s do something. Okay, fine. If you you''re happy to do wakeling, can
  we. I mean, does is this time work for you? Quickly?'
- 'Me: Yeah. Yeah. Yeah. Yeah.'
- 'Them: Yeah. So wonderful.'
- 'Me: It''s. There will be some Fridays I can''t do. Sometimes we go away for the
  weekend. But it''s not. There''s. There''s nothing in the near future. We can always
  move it around, can''t we? Let''s just put a line in there. And then we can move
  if we need to.'
- 'Them: We done? We can skip from time to time. We''re going to get bored of each
  other, so. Yeah, we can. Yeah, that''s fine. Okay, I''ll make it. I''ll make it
  regular. Well, not every week, anyway. Yeah, with a few exceptions. I will make
  it regular. So, you know, we can always escape if it doesn''t work or we have lots
  of things.'
- 'Me: Well, it''s. It''s good. It''s good to talk about this because, you know, all
  of you just come up with ideas, don''t you? And you only really realize them. I''ve
  recorded it again. Like, I''ve stuck this on Granola. I literally do it for everything
  now. And even that, it''s amazing what it pops up with.'
- 'Them: Pretty addictive. Anyway, but just go. And again, I''ve heard there''s somebody
  from, from a previous call with a client and I, I just got. And the summary starts
  for good. And again, we''re always scratching the surface because this templates,
  these recipes and all these things with Granola make. When I say circulars, we''re
  probably getting 70% of the value anyway. But this. There''s more that. Anyway,
  I mean, just that. Just the basics is. Is plenty.'
- 'Me: And that''s all I use, because I''m just using the raw data. I''m just using
  Granola as a way to gather the data, put it into the Google Doc, which you told
  me about, using Zapier. And then put it into. Into the system. Fantastic. That''s
  a great way to do it.'
- 'Them: Did you send? Do you give cloth? All the trans. All veterans. All the transcript
  or the notes from Granola?'
- 'Me: Yeah, all of it.'
- 'Them: Because, I mean, I only did it. I''m always thinking of tokens, which just.
  I think I. I got traumatized with tokens that first week, and I can stop myself.
  But. But the summaries are really so good. But yeah, I mean, transcripts. I mean,
  you have calls that can take go like this one, right? By the way, that''s fine.
  I got footnotes. But I can always provide the transcripts if needed.'
- 'Me: Yeah.'
- 'Them: But I''m just thinking if I''m missing out something. But I find the note
  so good that I don''t really. I don''t know, I may be going. The transcripts may
  be good for kind of exploratory calls with new clients, but the regular calls. Sorry,
  I''m just thinking. Out loud.'
- 'Me: No, no, it''s fine. No, you''re right, because there may be some nuance in
  there that you''re missing, or there may be some detail that the summary is not
  actually capturing. And you could always go back on there and ask, you know, did
  the client ever mention this? Well, that might not be in the summary.'
- 'Them: I found myself going to Granola about a couple of things. So I wasn''t sure
  about the dates of a promo. I went into Granola and asked, what were the dates of
  the promo? And Granola is great. I mean, they may be using gold code in the back
  end. And it gave me the perfect answers. Now I could have get the trusted in through
  clothes and then ask the question to close and probably that would be better because
  then I have all the information I need there.'
- 'Me: And I don''t want to go anywhere. I don''t want to go to multiple places. I
  think that''s the thing. I don''t want to be going to all these different places
  to get data. I just want to go to Claude and say, go and get me the data, wherever
  it is. Did we ever talk about this with such and such a client? Well, it could have
  been a teams meeting. It could have been a Granola import. It could be in an email.
  I don''t want to have to go to three different places. Just want to go to one and
  say, give me all the details about this. It''s ever been discussed. And it''s just
  so annoying with teams just having to cut and paste. Bang. But remembering to do
  that, I''m setting a task to do it. You know, so that every. I''ve got recurring
  tasks every seven days or something. It''ll pop up. And I say, all right, I need
  to do that. And then because the task. If I say completed, carry out this task.
  Save. Put that into process. My notes. I put that into Claude and it goes and reads.
  So what''s happening in task is when you. When you take my notes. It copies that
  into downloads folder. Then I go to Claudia. If I say process my notes, it will
  read that download folder. And then go and do whatever I''ve asked it to do within
  the. Within the task. But everything''s visible in the task. I think that''s the
  nice flow of all that, that you don''t need to remember the detail, that you''ve
  already saved it within the task. And you don''t need to know what to say to Claude,
  because it''s already in attack what you. What you want to achieve from it. So it''s.
  Yeah, it''s just a. It''s just a nice kind of flow to it all. And certainly it''s
  all done within. Within Claude as well. It''s proper techie, though, isn''t it?
  I feel a proper geek. Really do feel like a geek. It''s great.'
- 'Them: I''m thinking, what next? I''m thinking, okay, this is Google Ads, but what
  next?'
- 'Me: Yeah.'
- 'Them: I''m thinking about other projects because, as I said, everything is possible
  now. So all the things I thought of doing that it felt, well, you know, I''m not
  going to have two years to build this. I can build in two weeks.'
- 'Me: Yeah, yeah. Yeah. I tell you one thing to be very careful of. If you go down
  the Microsoft ads mcp. That is a bitch. As ever, Microsoft ads is a pain in the
  ass. You''ve got to use an Azure Cloud account to do it. I was on the phone. For
  pretty much two hours with Microsoft trying to sort it out. It was just a nightmare
  to the extent where I''ve set it up, the necessary links and so on. I''ve not even
  touched it since. It just sucked the lifeblood out of me. And you think, well, I
  don''t. I don''t really. I''m not up to date with Microsoft ads as much as I am
  with Google Ads, so maybe it''d be a good thing with code to use it to. To optimize
  things. I can''t be asked. You know, the amount of money it generates. I cannot
  be bothered at all. It''s the usual thing. What do I do? Do I spend an hour on Microsoft
  ads or an hour on Google? It''s a no brainer, isn''t it? You know, I''d rather spend
  an hour doing bloody recipe cards than being on my consultants.'
- 'Them: Here. It''s getting worse. So destroying going through the amount of Microsoft
  ads a ui. It''s just like what I''m doing Megaway.'
- 'Me: Yeah. Yeah, yeah, yeah, you''re right, you''re right.'
- 'Them: Anyway. Well, have a good weekend.'
- 'Me: Lovely. Yes. Enjoy that. Thank you, sue.'
- 'Them: Take care.'
- 'Me: Have a good mate. Bye bye now.'
client: grain-guard
source: Google Docs (Zapier)
imported_at: '2025-12-18T14:41:12.337554'
processing:
  client_detection:
    detected: grain-guard
    confidence: 80
    method: title
  ai_analysis: false
  model: null
  action_items_extracted: 0
  tasks_created: 0
---

# --- Enhanced Notes ---

**Date:** 2025-12-18 14:41

## Processing History

**Imported:** 2025-12-18 14:41
**Source:** Google Doc (Zapier) → Granola API enrichment
**AI Analysis:** ❌ No
**Client Detection:** grain-guard (80% via title)
**Action Items Extracted:** 0
**Saved to Markdown:** Yes (Google Tasks deprecated 2025-12-16)

---

## Attendees

- -- Enhanced Notes ---
- ### Current Claude/AI Development Excitement
- Both feeling transported back 15-20 years to early programming days
- Similar excitement to when Sergi started with Google Ads in 2005
- Peter feels like he’s rediscovered the joy of coding
- Everything feels possible now with modern web development technologies
- Node.js, Express Server, Flask apps
- Cloud deployment via Railway for web server hosting
- ### Peter’s Recipe Card Project
- Built system to digitize Gusto meal kit recipe cards
- Takes photos of front/back of cards
- Extracts text automatically into searchable format
- Kids can search by ingredients (e.g., “courgette and chicken”)
- Demonstrates rapid development capability - completed in \~30 minutes
- Planning web deployment via Railway cloud platform
- ### Development Workflow Preferences
- Peter uses raw terminal screen with Claude
- Prefers text-based interface over formatted chat
- Uses bypass permissions flag to avoid constant prompts
- Often runs 2-3 hour development sessions
- Sergi primarily uses chat interface
- Finds prompts manageable for smaller batches
- Typically works in 5-minute increments
- ### Peter’s Advanced AI Knowledge Base System
- Building comprehensive brain dump system
- Pulls from Google dev blog, industry experts (Brad Geddes, Frederick Vallaeys)
- Updates weekly, monthly, quarterly, yearly
- Indexes content properly using SQLite
- Strategic decision support
- Analyzes context for Google Ads optimization decisions
- Suggests alternatives based on knowledge base
- Acts like having an apprentice
- Integration with Google Ads management
- Writes strategy reports and client communications
- Implements changes directly via API
- Includes mandatory validation protocols (backup, dry run, verify, restore)
- ### Advanced Google Ads Automation
- Asset text optimization system
- Pulls headlines/descriptions from PMAX campaigns
- Analyzes 90-day performance (CTR focus)
- Categorizes underperforming assets
- Generates 15 alternative text options with dropdown selection
- Experiment tracking system
- Logs all changes with expectations
- Creates follow-up tasks for 4-week reviews
- Provides categorical success/failure analysis
- Client example: $9 million Q4 US sales for toy client
- Handles rapid budget changes during peak season
- Automates email responses and change documentation
- ### Sergi’s Productivity Systems
- Live audit system
- Reduces audit time from 6-7 hours to 30 minutes
- Built from scratch rather than using existing templates
- Meeting preparation automation
- Pulls from Slack, emails, meeting notes
- Generates formatted Google Slides with client logos
- 10-minute prep vs 2-3 hours manual work
- Automated reminder system
- Scans communications every couple hours
- Sends Slack notifications for tasks/reminders
- Integrates with custom dashboard for approval/deletion
- ### Dashboard and Task Management
- Sergi’s comprehensive client dashboard
- Task management synced with Google Sheets
- Client engagement scoring system (60-90 points weekly)
- Health monitoring for caches and systems
- Engagement gamification
- Points for calls (30), emails (varies), Slack messages (5), Google Ads changes (3)
- Adjustable targets based on client payment/demands
- Red zone alerts for neglected accounts
- Template workflows for recurring tasks (promos, sales periods)
- ### Technical Integration Challenges
- MCP server implementations
- Shopify integration working (requires app setup)
- WooCommerce integration functional
- Google Trends problematic (timeouts, API limits)
- API cost management
- Claude Max covers cursor usage
- Separate Anthropic API costs for independent agents
- Recommendation to use Haiku for cost efficiency
- Skills vs API limitations
- Web UI cannot access cursor skills
- Forced return to terminal interface for full functionality
- --
- Chat with meeting transcript: [https://notes.granola.ai/t/86d253a0-72f5-4a7a-bb96-87e3237ba898](https://notes.granola.ai/t/86d253a0-72f5-4a7a-bb96-87e3237ba898)
- -- Full Transcript ---
- Me: Hey, segi.
- Them: Hi, peter. Hello.
- Me: Yeah. Good.
- Them: Yeah. Good.
- Me: I've got. It's Friday, I must say.
- Them: Yeah, well.
- Me: So tired.
- Them: How's it going?
- Me: I feel like I've been transported back about. 20 years, 25 years back to being a programmer. And being excited about code, and so I've not been able to walk away from your desk.
- Them: Look, I didn't say 25. I was thinking 15.
- Me: Oh, okay. Thank you very much for that. I appreciate that.
- Them: Thousand. Well, I'll get. Fine. Didn't sound the way it went, but anyway, I thought exactly the same. I thought exactly the same. Right. I was thinking about it just 10 minutes ago. I was thinking, how do I feel about this? And I was thinking, it feels like the self excitement I had. Well, I say 15, but actually now it's more 20, because 15 is when I got into Google Ads. Yeah, that's the sort of thing I got back 2005. When I. I started playing up with java. And, you know, and all these things, you know, getting deep into programming, and that was actually.
- Me: When you've enjoyed it. When you enjoy doing it as well. That's the thing that gave me the buzz.
- Them: Yeah, yeah, yeah, yeah.
- Me: I'm glad you feel the same. That's brilliant.
- Them: Exactly, exactly the same. And. And actually thinking back, so before starting at Success, that was obviously on my own, doing work for five, six, six clients. I was thinking. Look, this is not going anywhere. I'm not really loving it. I know. You spend four very intense months. Learning about Node Lending, about Express Server. So all these web development technologies that have been, you know, created, that were new. That didn't exist. When I was building, you know, from its clothes, so to speak. 15, 20 years ago. So now, obviously, everything has changed now.
- Me: Yeah.
- Them: And everything is possible now.
- Me: Absolutely right. Absolutely right. Everything is possible. That's a really good way to describe it. It's really strange. Isn't it? I'm using. What's a flask app? I have no idea. I don't know what railway is. Railways to run an app on it on a web server. So you can run a cloud app on a web server and access it anywhere. Yeah.
- Them: Do you think my way? I started using my weight yesterday. Yeah, yeah.
- Me: So. And it was a crazy thing. I said, we have. It's got to be called gusto. I don't know whether you were aware of it in the UK when you were in the UK with you had it or not, but basically they provide the menus and the ingredients. For meals. So you say, right? I want to buy four meals. I want this one, this one, this one and this one. They send you the fresh vegetables and all the rest in a box. With all the meat. All the rest of them come with four cards. If you got four recipes and you follow the recipe on it. And it's fabulous food, absolute, like, techniques you wouldn't normally use. It's not cheap, but it's really good with eating some fantastic stuff, even though it's a good cook. Anyway, it's different stuff. So I thought, okay. What if I took a pitcher of the front and the back of that card? Made it into a recipe and then put it on the web and made it searchable. And then the kids could access all those recipes. So you could say I've got courgette and chicken. What have you got with courgette and chicken? In and it would go and pop up the recipes. Yeah, done that. So actually taking a photo of it front and back, it reads it, it puts it into the right sort of floor mat and it puts it onto the Internet. I've not got the Internet bit yet because I've not got the railway bit, but that was like half an hour.
- Them: Sorry. Are we talking about pushing recipes? Sorry I lost you there. I thought it was. It was as it was an example. And then I realized you were talking about real thing.
- Me: Yeah. It was a real thing. Yeah. So we got these cards, these recipe cards. That from Gusto, I thought, take a picture the front and back of them. And there's photos on there, there's all sorts, but I just wanted to get the text of it. And they're in the same format. It's got the nutrition on there. It serves this many. And then it's got the actual process, but it's got a list of all the ingredients. Above it. So I'm going to put that onto a web server. So that the kids can go onto that web server, given the password, and they can go look for these recipes.
- Them: Okay?
- Me: So they're all searchable. And it was just a bit of fun. And this is like you got your four things running. You think, well, I've got a spare one there, let's do it on there.
- Them: Yeah, he's like a waste if you like. I mean, you have three screens, so why not have three things building at the same time? I have all this chat tabs and I have two, three working at the same time. I sometimes think, well, why don't I have a fourth one? And I'm building something else.
- Me: Something for a bit of fun, yeah?
- Them: Right. For fun. For fun.
- Me: Now, the interesting bit is, okay, so actual technique there. Do you use terminal? Do you use chat? On cursor.
- Them: I mostly chat. Very rarely I need to use terminal.
- Me: So I use the raw terminal screen. I'll just type Claude into when it pops up. Type Claude in it, does it? It's not. It's the pure text version. There is the chat version, isn't there? Which is a little bit more formatted. I don't actually use that anymore.
- Them: Sorry. By the way, this one? I said five. Okay, go ahead. Here.
- Me: So if you call it terminal, in chat, in cursor. So the one thing I've done is I started up doing Claude. So I just run claws and it pops up and you can go and use Claude in it. So then I've done. What Mike's done is using the abbreviations. And done the version where. What's the name of it? There's the flag which says ignore any sort of input at all. Just run it. And it just blasts its way. I can't remember what it's called now.
- Them: Composite.
- Me: No. Damn it. What was it? I'm normally talking into this. It's weird typing. Because normally it'll prompt you, wouldn't it? It said, do you want to use Bash? Do you want to do this? So you can actually set the flag that just goes. And it just blasts through it.
- Them: This is not what you explained the other day. How did you call it?
- Me: 's a really weird.
- Them: Can you tell? Very composer.
- Me: No. It's a flag to use with Claude. When I find it, I'll let you know.
- Them: You asked for a feature or something, you enter the prompt and what would normally happen is that it would ask you confirmation to things.
- Me: Correct.
- Them: Sometimes you get yes. No. Sometimes you get yes. Sometimes you get yes to everything like that.
- Me: Yeah. One, two or three? Two. And one and. Yeah. Make sure you're awake. Yes.
- Them: I normally go at some point. Maybe the first part, they say yes. And the second one, when I know it's going in the right direction, I go yes to everything. And then I move on. I come back five minutes later.
- Me: Yeah, there's another. There's another version of Claude where you can run it with a flag. And basically you just leave it. You say, I want to do this, this, this, this and this. And it goes. And it just rattles it off. And there's very few prompts. You got to be careful with it. It's actually doing the right thing.
- Them: Okay? Yeah, I. Don't find I don't find the prompts, I don't find I get too many problems. I don't think I'm being delayed. I mean, it's not like. Look, we have to build this today point, okay? The client is like, okay, fine.
- Me: Yeah.
- Them: If I get. Look, I don't think we'll make. I mean, if I'm the scientist correctly, I don't find it particularly annoying that I get prompts from time to time. And when I get the option, normally just go for yes to everything and it leaves me alone. And to be honest, I work in a small batches, so it's not like I want. I mean, I don't expect to add a prompt. I will require an hour's work. For Claude. Normally within five minutes.
- Me: Oh, gosh, I've been to two or three hours.
- Them: The time.
- Me: Just on one thing. When I'm planning something, I'll just put two or three hours. It'll just go and do it.
- Them: Okay? Okay, let's go. Okay, let's go. Where are you building that will require two, three hours of work every day.
- Me: I'm building my brain, Sergey. That's what I'm doing. I'm building my brain. Okay?
- Them: I wish you.
- Me: I'll give you an example. I'll give you an example. So I've got a knowledge base. Right. I'm at a stage now where Mike produces something in his brain. And I'll pull it in and I'll say, what's in Mike's brain that I could put into mine. And I've got to the point now. He said nothing. Yeah. There's nothing that you can do. There's nothing you can add from Mike's brain to yours where he's doing it better. Because the thing with Mike is. And that's not an ego thing. He isn't running an agency. A lot of the stuff he does isn't agency stuff. And when he goes and does the CSV analyzer is very good. I really like that one. That is very good. But most of the other stuff, like where he's doing the search terms, I'll put it into high and medium, low intent. You just go, yeah. 20 and it's got tired. It couldn't do anymore. Well, I've got 100,000 in there. What am I supposed to do with those? How am I supposed to categorize those? If you want to do over a big period of time and make it worth your while. So I don't tend to do touches. But one thing I did do at the beginning was I wanted a knowledge base. The key to their brain is that we are doing a brain dump. We're actually saying, these are all the things that I know. These are all the things that the Internet knows about what I know, what I do. I want to put them all into a knowledge base. And I want to keep that up to date. I want to be looking at the Google dev blog on a regular basis, see if there's anything on there that's interesting that I might find interesting and bring it in. It's something Brad Geddes is doing that's interesting. Frederick Valets what they talk about search engine life, all those. So I started doing that, and I pulled in. I said, go and find me some websites with Providence and people with Providence and pull it all into a database. Mike then was talking about his brain was talking about using SQ Light for doing indexing. So it will actually index it properly. And then I took it at stage further. The other day. It's like taking a stronger and stronger drug, isn't it? You just push it a little bit more. So now the knowledge base will update every week, every month, every quarter and every year. And it will basically mash it all together, all the stuff that's being talked about. And I can either search it and say, what's the latest thinkings on pmax optimization? Or I've got it now and I'm still not sure how it's going to work this because we literally finished yesterday. But when I make a decision, a strategic decision in Google Ads to say, I'm going to do this on this client, it will then go look at the knowledge base and say, I've got this context about that. And maybe you want to try this or maybe you want to try that. That's what I'm aiming towards. But it's like having all of it is like having an apprentice. And you say, can you go and do that? And you go and give it some work to do. And it comes back and you read it and go. And I've said it to before, that's rubbish. That's absolutely rubbish. Because of this, this and this. You're absolutely right. I'm fed up with it saying that, but you're absolutely right. I didn't do this. Or I didn't do that. I'd done a report for a client and it was completely wrong. And he said, well, I didn't really wanted the latest data. What do you mean? Well, yeah. Then you build stuff in like that. I'm now using it. So you said the top five, but they're all kind of blended together. But I got it to a point now where I'm writing stuff back to Google. So I've got a client now where there's some big budget changes, so I've done a Q4 strategy report for it. And then said, give me that strategy. Let's go and look at it. We find all the strategy when the budget changes need to be based upon last year's conversion rate increase and decrease because of Black Friday, Christmas and all the rest of it. And then I'll say, do a report. Write the email to the client, write me a team's message to the client, formatted nicely and then affect the change. So I was prompted by Mike saying about hooks, actually putting a hook into it. So whenever this happens, always do this. So I'm thinking, okay, what I actually want to do is when I make a change, And to get it ready to send through to Google. I want. It to back it up. Back up the existing position for whatever it's looking at. Do a validation of the data that's going in prior to it going in. Make a run, a dry run, make sure it works, then do the live run. And then verify that what you asked it to do. Has, but then always have a restore position. It didn't actually work the other day, the restore, but that's a different story. So I was doing that as a hook. I think every time you try and change from Google Ads, do this process, it doesn't actually work. It won't do it on an API, a hook. But now I've built it into my context. MD that this is a protocol, a mandatory protocol at the top. Do this, this and this. It's brilliant. Eden's the point where if you're in this super duper mode where it's just blasting through, it would stop and say, I'm going to do this now. Are you all right with this type? Yes. To continue. So you can read what it's saying. Type. Yes. And then it will go and do it. That was a belt of that. That was. I really like that one. But I'm doing more and more of that writing stuff back into Google Ads, which is quite scary. And I just tend to. Download into Google Ads Editor, do the change. And then download to Google Ads editor where all green bits highlights are and just see what I mean. Change the right thing. I said it's caught it a couple of times, but it's not done what it's supposed to do. But a lot of the time it doesn't re enquire on the Google Ads data through the API. You got to really tell it that I want the latest data. And then it will tootle off and do it. So I'll go on. Your turn.
- Them: Yeah, yeah. I've been thinking about things like that, but it's like, I don't know if. I don't know if it's the way I work or is the type of clients I got. Maybe I'm lazy. I don't find very often that I have to do. That much work on the Google Ads account. So it's more about you set up a new campaign, I mean. Just to get stuff, just to say in terms of search campaigns really is just. Outside from brand campaigns. It's only two clients where you really use search. The rest is mostly shopping. Or is it mostly is pretty much all shopping op Max. And then we have a marketing mags. Do we need by hand? It just feels right and I wouldn't be optimizing it. So. What sort of so are you talking about? Maybe, I don't know, your hotels client when you have to create many campaigns and I don't know.
- Me: No, not necessarily that. One of my favorite ones at the moment. It's very nearly finished now. This was prompted by a client who's changed all his text outside my control. Changed all the text in his ads, but Black Friday all over it. All over it. Now he wants to revert it back to Christmas, and then he wants to revert it. To. So I said, well, you do that. You change the text. There you go. There's the spreadsheet, a G sheet. With your latest position, with your headlines in your descriptions. You can go in and change that, and I'll suck that in. And that's pmax and rsas.
- Them: Okay, so that's you telling Claude, go and take this.
- Me: No telling the client, I'm saying. So I've pulled in the latest position as though you were going to do it in Google Ads Editor. But all it says in the sheet is the text assets.
- Them: How the height.
- Me: I've actually looked to do image assets now as well, so you can change those. They're a bit tricky because their IDS. But download it into a G sheet. So you got one sheet for pmax, one sheet for rsas. He's landed me in the ship because he just got rid of who was effectively my boss. I've never had a boss for many years, but she said she was my boss anyway. So he said, I'll help you out with the text. I'll do it. Right, fine. There it is. There's the sheet. You tell me when you finish, and I'll suck that back into Google Ads. It's been a bitch to do. But off the back of that. I've got something that will pull in. Apmax campaign. The asset text from a PMAX campaign. So headlines, descriptions, long headlines. It will pull it in. It will tell me how they've performed over the last 90 days. So really click through rate and conversion rate. I'm more interested in click through rate than anything else. Then categorize them. Which ones need changing, which ones have gone stale or just aren't working? So it will look at it. As a client base, not just saying, is it less than 5? So look at that asset group. Highest is this lowest is that. Which one should I actually be looking at? It'll bring them back in a list. I just want the high, the high priority ones. So the ones with the very low CTR, and it'll tell me what the CTRs, what the conversion rate, what is the conversion? It will tell me why it says it's a high. It'll tell me what the current text was, and then it has a cell. With a drop down List of 15 alternatives of text that I got clawed to do based upon criteria that I've set for all the clients. So it'll go and look at them, it'll look at the URL. And it will bring me back a selection of different ones. So ones that are technical brands, quirky CTAs. Give me a choice of those. They all keep. Then I can send it back again and it replaces those. Assets. So it's an optimization thing, and it's something that. To do that manually. Once I get it right. It's nearly there. To do that manually would take a long time. It's something I never do. I never, ever do that. I never go and optimize my asset text. And you look at it, it's lying you through. Top 1. Top ctr 8%. Lowest 0.4. Why would you want to keep that one? What a difference that will make.
- Them: Well. Okay. My view probably not a lot. Sorry. I'm saying this because I go through these reports quite often and what I see is that for big enough accounts, and that's different story when you're spending £20 a day and we're gonna have the data and there will be wastage there. But for, you know, big enough accounts, you can see the best performing ones, the best performing headlines based on descriptions, the ones that perform, that tend to get the most impressions. But no, you're right. I mean, there is that. And there is also the fact that you have maybe 50% of the headlines that are underperforming. And still spending, you know, some amount. So it's the case of why keeping them there. If you remove them, yeah, it's gonna be small impact, but that's the saving. And maybe that stops you from trying new headlines. So there is some truth in that. But. Yeah, I mean, I always think. The lazy me always think. Look, is it worth the effort if it's gonna move the needle in a meaningful way? And maybe just ask me. You know, just. Okay, that's an excuse.
- Me: You fit the nail on the head. So if you've hit the nail on the head there, because you asked the question before, why do it in Claude? Why change it in Claude? And the reason is I've got an experiment system that is logging when they go in. Is creating a task for me to go and looking back in four weeks time to see whether they worked or not. I will know categorically. Whether that has worked. And that's why I'm doing things through Claude. Because I'm logging things. I know we can go into change history, but there's certain things not done in change history. And in change history, you can't say why you're doing this. So the experiment system I've got is it says this is the expectation that you've got. Let's go back, let's set a task, because I've now got a task manager system as well. And prioritizing tasks. And it will pop that up as a priority, so you need to go and test this. And the task manager. When it sets the task, it'll put in it in a great big chunk. This is why you're doing it and this is what you've got to ask. So I go right. Add a note to the task. Save it, put it into Claude and says, process my notes. And he would have dragged all of that into Claude. And he'll say, right now, go and run this. And it will go and process that task. And do the things I want so I don't have to remember it. And there's little, tiny little things. That I've changed. It's working. Is this not working? And you look at it go, no, categorically that's worked, or categorically, that hasn't worked, and you may not have come to the same conclusion. If you've done it manually because it has got all the facts. Not necessarily a snapshot, but you can go back on the API and see what the position was before and look at it now and go, there you go. I think this. What do you think? Now? 50. 50. I'll say. No, I think that's bullshit because you've not done this. You've not done this. But a lot of times you go, oh, that is very good. And it's because you have logged it. In clothes. I'd love to do everything in Claude, I'd look to not touch the dashboard at all the Google Ads, ui. But that's never going to happen for a long time. But it's been really handy. Really handy.
- Them: I'm not going that deep into Google Ads at all. At all. I've been. Distracted about when you mention a dashboard you transportation list. I go down that route as well. So I would say probably a lot of my time with Claude.
- Me: Great.
- Them: Has been a lot, not everything. But what has been on productivity. So, for example, to have few things that build. So in terms of Google Ads, a couple of things I got, I've got, I've created what I call a live audit skill, which I don't know if I was, I don't, I don't know if I use one of mics as a does not as a draft, as a template.
- Me: Okay?
- Them: And I think I created one from scratch. It has been very helpful because I had a couple of audits reviews for potential new clients. So look.
- Me: He has a no.
- Them: I'm able to do in 30 minutes. The other day. I just had a presentation this morning. Got a potential new client. Not, not. Not particularly interested in this one. But point is, I did in an hour what normally what it would have taken me otherwise, six, seven hours.
- Me: Fantastic. We talked about that, didn't he? That is brilliant. Absolutely brilliant.
- Them: Six, seven hours. Yeah, yeah. That was the first attempt. I was building it and going through, so now I've had it. Next time it's going to be a lot easier, not faster.
- Me: Did you feed in your existing audits to that, then?
- Them: Second. No.
- Me: Did you feed? No. Okay.
- Them: Yes. And now? Well, obviously, I. My promise included all the things, all the questions, all the knowledge. But no, I did not.
- Me: See, that would have been my starting point, I think. No criticism. It's just another way of thinking. But I would have fed in all the audits you've ever done. And say I'd want to create. Go into plan mode and say I want to produce a system that produces what it's like this. Off it goes.
- Them: Okay? Maybe.
- Me: Have you used Ultrathink yet?
- Them: Ult I think.
- Me: Ultrathink. Ultra. It's fun because it does it in a rainbow color. When you type in Ultrathink, it comes up with rainbow colors for the latter. So it's worth just to do that.
- Them: Is that? Is that. I would say that is that. Is that a cursor in cursor is saying.
- Me: Yes. Yeah. Yeah, yeah. If you're running Claude in cursor, in terminal. If you're right, ultrathinky. Or write it. Alternating colors and letters.
- Them: So if I. Let me share my screen.
- Me: Yeah. Sure.
- Them: Sorry. I'm trying to find. Okay. Yeah. Here you go.
- Me: If you try Whisper flow out yet.
- Them: Yeah, I'm wasting all the time. Make fan. I'm getting used to it. Not in paid mode yet, but I may. Well, I think I will agree soon. And what? What do you want? To show you. Okay, fine. So we are. Sorry. So is that. Did you say ultra? What is it? Is that. Is that.
- Me: Ultra. Think.
- Them: Is that here? Where would I find it?
- Me: I can't see screen.
- Them: How you. Oh, sorry. Why not? You cannot see it. I'm not sharing anything now.
- Me: No. No.
- Them: Okay, let's try again. Now.
- Me: Yeah.
- Them: Yeah, okay. So what is it?
- Me: Just type in ultra thing there.
- Them: Ultra thing.
- Me: Yeah. No gap, no space. Right. It must be in Terminal then. Can you go into Terminal? Is it Command T or something? That's it. So if you go into Claude there.
- Them: This is what you mean.
- Me: Yep.
- Them: Okay. This is how you're using it.
- Me: That's how I use it. Yeah, all time.
- Them: Then. Okay?
- Me: If you do one.
- Them: So, you know, using this chat box.
- Me: I use that all the time. I've got four of those going any one time. So if you type in if your query there. And you use the word ultrathink in there. Just type ultrathink. Now, that's the fun bit to start off with. There you go.
- Them: So is that it?
- Me: But it's really handy because, you know, you could use. You could use Opus Force on it, whatever it might be. Using ultrapync, uses the most powerful model. But you can do it per queries. You're not paying a huge amount of money for it. So if you. If you would. If you wanted to do some analysis, say you wanted to do analyzed Black Friday results for such and such clients. Comparing with last year. Ultrathink. It will take longer to do. It'll do a deeper thinking. Most of my stuff I use Haku. I've got it to default. All the agents and launch. Most of the agents and launch agents use Haku rather than sonnet or Opus 4.5. Because they're more expensive. I know he dropped down every now and again or go up to this. That's a great way to do it.
- Them: So you go. You go ultra think and then you type. Then you press enter, I guess.
- Me: No, no, no. You just. You just use the word ultra in your.
- Them: The question.
- Me: Prompt.
- Them: Analyze. Analyze search. Intent for client? I don't know. Campaigns for the past 30 days.
- Me: Yep.
- Them: Is that what? You okay? Fine.
- Me: So just. It will take longer to do it.
- Them: Okay? So tell me, tell me again. Why is this better than just going through this box? And just, like, asking the same question.
- Me: You know what? I don't know. I just prefer it.
- Them: Okay, fine. Okay.
- Me: I think part of it is because I'm from a Unix background. And I just get really excited seeing UNIX commands. I'm doing IT backup and it says tar. And he's going, bloody hell, tape archive fantastic. I'm old enough to know what it means. It's like grep grab expression. Orc.
- Them: The type one is not very. I find it not very responsive. I don't know. But. No, I mean, you're familiar with it, that. That's where you.
- Me: Well, let me share my screen with you. I think it's fun to see the way other people work, isn't it? Because we're giving so many different ways to do it.
- Them: Oh, wow. I mean. This. Oh, my God. Oh, my God.
- Me: That's the way I work. And it's like, as you say, I've got this. Oh, he's still waiting. There, let's hit yes on there.
- Them: And of course, of course, this is just one of screen.
- Me: Yeah. Well, this is the three sessions I'm doing. If I go up here and just split that. If I do ca. I've got an abbreviation for this. It's got bypass permissions on now. The bottom there. You see that?
- Them: Yeah, yeah, yeah.
- Me: So that's the bit where it doesn't ask. Like I've got that middle one said yes or no. Sometimes I might want to look at other times I just want to blast it through. I don't want to be interested. But if I do shift and tab on this one now, I can still go to plan mode.
- Them: Yeah.
- Me: So, you still there?
- Them: Yeah.
- Me: It's just kicked up another screen because. I've lost reset. You've actually completed there, so keep that with me a minute.
- Them: I'm still seeing your terminal.
- Me: What on earth this happened? There. I've just lost the. There we go. Does cut it. What was I saying then? Yeah, I can still scroll through these so I can go into plan mode if I wanted to. Shift and tab bypass Shift and tab. Don't know what that one is, but then accept edit on. So if you start it with this flag, you can still flip between all the others. If you wanted to step through it a bit more, you can still use that. Accept add its own. Or if you wanted to do something quick, you can just do bypass permissions on.
- Them: Yeah. Yeah, okay.
- Me: I do find that really interesting.
- Them: Yeah, indeed. I mean, you have tasks going on for hours.
- Me: But that's what happened with the. With the. Doing the. The knowledge base one, because it then went off. It found a whole new load of articles to go and do. Had to do a web pool for all them. Sorry, a web fetch. And then stick them all into the database, and then. So I'm just leaving that running. Another really interesting one is doing unit tests. That's one of mics that where you. You say to it run or, or you can do some setup. Unit test or run unit test. Specify unit tests. And the unit tests go into your code. And test it all. And it will toot laugh. This stuff it found I was getting dead locking. I was getting old scopes were wrong. It was. It saved me so much time just using unit tests. And it will just. I say one of these. It'll just run through. It'll just keep running through. And said, so many passed. I'll do them in phases. I think these are important. These are important. These are important. It'll run them and then carry on.
- Them: So you need. You need tests. Okay, unit test.
- Me: Your project.
- Them: Your project, your. Your agents as well, I suppose.
- Me: Everything? Yeah, everything. Yeah.
- Them: Okay? Because you have staff running all the time, right?
- Me: I've launch agents running. Yeah. And they. I've got an agent dashboard now. I got to keep my eye on them because every now and again they'll just bomb out. And I've got one thing I found was because I'm switching my computer off every night, so if I set a schedule, They weren't running, I'd set them for 6:00 in the morning, start at 7. So now there's that flag that says, if they've not run already, then run them. And now I've got another thing that runs. I've got a health, a slash command. So I've got health and it'll run that command, that skill. And it'll just. It'll blast it through. Make sure everything's working. I've got launch agency. It'll just go and start everything.
- Them: Yeah.
- Me: Seriously, all this stuff about the electricity and cloud servers and AI taking all loads and loads of electricity, it's me. It really is me. I'm just totally addicted to this thing. I think it's fabulous. And this, you know, the most important thing. There's stuff I'm producing for my client is extraordinary. I did. I did a landing page report for a client the other day, and it happened to have failed the landing page report, and it was like that. And I put screenshots in of the landing page before and after and what I was testing and why it had failed and why I thought what we could do in the future. And she just put one sentence in. How does the landing page test going? And I set this thing back and I went, christ, that is my. Fee for a month doing that, to actually produce that in that level of detail. Would have taken me a day at least, and I just rattled it off in maybe an hour because I wanted to really over ag it.
- Them: So let me go through that. So there is a landing page test, which I assume means that the client created a secondary landing page.
- Me: Correct.
- Them: And I don't know, maybe you have a campaign. 50% traffic going to one page, 50 or the other.
- Me: It's an experiment. It's an experiment on Google Ads. Experiment.
- Them: And he asked you, well, how is the experiment going? Fine. And you go and tell Claude the client is asking me this.
- Me: Yeah.
- Them: Based on the context information and.
- Me: No, I didn't do that. No, I didn't do that. I said email sync. It ran the email sync. It's labeled the emails for clients. I said, read Helen's latest email and comment on it.
- Them: Okay, I comment on it. And then you get the response what it does. What?
- Me: Well, it produced a report or only page report? I had to do the screenshots of the so desktop and mobile for both of them. I said, drop this in there.
- Them: It was a critique on the landing page or it was just data.
- Me: Is it? No, it's a test. So I. I sorry, it was. I didn't explain that very well. It was an experiment in. In Google Ads for an ad variation. They had variation was landing on different pages. So it was a. It was a landing page test as such. But the data was in. In Google sending it half and half.
- Them: Yeah.
- Me: So that.
- Them: So it got the data from the variant test and it just produced a report on that data. So you come and look. I don't know. I mean. What? What? I was just wondering. I mean, that is so. If it's landing page, it's more about conversion rates.
- Me: Yep.
- Them: It's more about cost per conversion and things like that.
- Me: Yep.
- Them: But you talk about screenshots, so what was that?
- Me: But the screenshots were the actual landing pages themselves. Where it was sending it to, so did desktop and a mobile version. And I asked it to critique the landing pages as well.
- Them: The landing page critique is it was the real valuable thing from.
- Me: It was. But we'd done another test earlier, another month. It was about that big of a review on that one, because I'd done it myself, and it was. It was quite favorable, this one. There was no conversions at all in the period for either of the variations. They're usually quite low anyway, and he told me why.
- Them: Okay?
- Me: It actually explained why.
- Them: So you have. Sorry, keep interrupting. So you got your. I don't know, maybe you have a skill that goes through landing page critique. Now. Okay. Just Claude criticized landing page.
- Me: Yeah. Yeah. Yeah.
- Them: Okay?
- Me: And as time goes on, what I might do is build some more stuff into my knowledge base. So the knowledge base now is being built upon going and looking on the web. It's built upon playbooks I've created for clients. It's built upon pro post mortems of them. Provides. I've just done one for Black Friday for a client. You know, we did this, and this happens. And my own knowledge. There's actually a section in the knowledge base which I've not run yet, which is going to be an interview phase where it's going to ask me things that I do, things that I think are good, things that I think about.
- Them: Yeah, yeah.
- Me: And I said to it, that's fine, but I don't want this to be my opinion. I want this to be statistics based, say. Right. Okay, well, I'll bear that in mind. So I might be saying I think we should be doing this, and it's actually wrong. Statistically, it's wrong. And I want to be pulled up on that. I don't want it to be my opinion. I want to be able to give it the input. And it's called the Rock Systems Methodology. So I want to give it that input, but I don't want that to be the. The total driving thing, because if it's wrong from the start, it's going to be wrong for everybody then. So that's why the knowledge base for me is the most important thing that is my brain.
- Them: Yeah, yeah.
- Me: The rest is access to to to Google Woocommerce. Got a woocommerce mcp server. I've got a shopify mcp server. That was relatively straight. It's a bit more complicated than the WooCommerce one because you got to create an app within Shopify. But now I can interrogate Shopify directly. Google Trends is a real shit. Don't bother with MCP for just awful keeps timing out, it just doesn't. Like it doesn't. It doesn't like too many API calls in one going. Google Trends does tend to use a lot. I won't. I won't bother with that analytics.
- Them: So shopify mcp and I. I don't have any shopify integration. I'm not going down the mcp road. What I do is I. I have an API libraries that the way that they. That the road Cloud took, which is fine with me. And. And one talks about mcp servers. And I feel like I'm missing out on it, but it's just, you know.
- Me: I don't know. Seriously, I don't know.
- Them: Yeah.
- Me: Sometimes you say, go and interrogate it and it'll go. I'll use the mcp. Oh, that's no word. I use an API direct API call.
- Them: Okay, sorry.
- Me: So I suppose I'm giving it an option. I just thought mcp servers. The right way to do it. Going back to go marble because they use MCP servers.
- Them: Yeah. That's why I I By the way, I I remember Marvel, there's so much going on and too many ten pounds here. I mean, in terms of AI anyway, so this Shopify could be very interesting as well. I think. Yeah. Because, I mean, in terms of, obviously, sales. Product performance, product stock. And. And things like. Yeah, I mean, margins as well. And. What? I wonder if that's something I use. I have. I have my. My Shopify. App, which I use, but it's not linked to clothes, it's linked to my scripts. And I keep. I have a number of reports taking data which I daily but that's not been integrated into Claude onto the grain. Like it could well be, anyway. Yeah, I've been working on something like that. So, as I was saying.
- Me: I know you can do this yourself, but I can send you the process for Shopify. I just drop it down and email it here? Want to pull that straight into Claude and say, I want to do it for that client.
- Them: Yeah.
- Me: Because it works.
- Them: Yeah. How do you. How do you use the Shopify data? What do you get permission to provide? Is there a stock, for example, gives me the best sellers or. Or what products I should. I don't know in terms of a stock, what products I should stop advertising because of lowest stock or what.
- Me: I've not scratched the surface. The only thing I've used it for, to start off with is I wanted to find out an overall roas for the clients.
- Them: Is.
- Me: Because they don't do much marketing elsewhere. So I tend to quote the Shopify figure. As the revenue and Google Ads is the cost.
- Them: Yeah.
- Me: So I don't know. The main thing for it. You got to jump through a few hoops. On Shopify to set up the API bit, and that was the pissy bit.
- Them: I've got that already, so that's. But, yeah, I mean, that. That's. That. That's exactly how I use it. So I get the client asking me, overall, I need the rows of six.
- Me: Okay? Yeah.
- Them: Upon. I have this in my dashboard, which sits outside cloud, anyway. It's monitoring that daily and that's. That's how it works. But it would be cool to have. But anyway, it's not integrated because I. I still want Anyway, it is not part of my. But in a way, in terms of what else I've been building, I mean, one thing I so there is that. There's this. I was. I was saying about the light review, which saved me a few hours, and actually, it found a couple of things I would have missed. But you're right. I didn't see that. I didn't. I will do probably will do that. Those, those audit reviews I like the most that will fit them into the quote and see how we improve. I mean, that's probably going to be what is the light review and more the high level, not high level, actually. The detailed review, the deep, the real. That's probably what I can do to fit, because I still want a different audit review levels.
- Me: Yeah. Yeah, yeah. And that's your. That's your value that you're putting into it. You know, to. Then you're going to get the reviews out in the style that you want them, and that is you. That's what you know, that's that. 's the bit you add to all that.
- Them: Yeah, indeed. Indeed. Yes, yes. And the formatting as well. So half a half scale and that. So basically, I have these calls and sometimes I don't necessarily prepare many of the calls because I speak into my clients and I've not done four years, so I really know everybody. But for some, for some others, you need to prepare those calls. So I have a skill that does that. So I just, you know, prepare. Prepare my agenda or my meeting prep, My meeting prep document. I think that that is an issue that was initially based on one of Mike's skills, but back on my call with clientex tomorrow morning,
- Me: Yeah. Yes.
- Them: And he just asked that. And he gets everything into a slide, a Google Slide with the right formatting, the kind of log, everything. So preparing something like this. Okay, I'll use it twice, so we'll see.
- Me: I look at you, I love it. You can't stop smiling about this as well. It's brilliant. Because that's exactly how I feel. Because you, inside your head, you go, wow, that's amazing.
- Them: Yeah. Because. I probably wouldn't have done that, but if I had to do that, he would have taken me two, three hours now.
- Me: Yeah.
- Them: He took me to the hours to get the whole thing done. But the following call, it took me 10 minutes. And it took me 10 minutes. So I prompted waited three minutes. Get these light show already. The formatting, the words, the titles, the log, all the dates, all sorted. It took me 10 minutes to refine because it's never. I mean, it would never be Find some of redundant stuff.
- Me: Correct.
- Them: But it was really good because obviously went through all my slack. It's like channel communications work through my emails, my nutri notes. So it came up with a couple of things. Oh, I had totally forgotten about this. Oh, that's my point. And to be honest, there's not so much AI in that.
- Me: Awesome.
- Them: The AI is summarizing all the communications and so on them into a cache and then getting everything into this slideshow or the document, the Google Slide. It wasn't AI, really. It was just the app.
- Me: Yeah.
- Them: It was just taking the formatting, so it was not. Claude. Create a Google sheet from scratch with the client. Logan. And no, this is the template. This is the cache with all the data. It's already summarized.
- Me: Yeah.
- Them: Now. Am I lying? No, I think I had much to do with that. And some of the things I built is reminder. So I'm not using agents yet, but I have jobs that run all the time. Or every couple of hours. So there's one job that checks my slack communications, my emails and meeting notes every couple of hours.
- Me: Yep.
- Them: Ten me as lack notifications for any tasks or reminders. So there is this email from this client. These are the three reminders. And it adds that into my dashboard, which is a task management tool I just built as well as you did. It just has actually four reminders and it goes hard to approve them or not approve them, accept them, or they delete them. And that's automatically just fits.
- Me: Yep.
- Them: So it's really useful for notes, for meeting notes, because Granola. So I have a call. Hang up, forget about it. And with the next hour, I will get reminded. These are the actions that go from Granola to growth into slack and from slack.
- Me: Yeah.
- Them: Well. And then into the dashboard. Into my dashboard. And, yeah, I've got that. And I cannot forget, really, and I kind of. Kind of focus on the next goal. And then after, you know, just go. Okay, These are my notes, are the actions. Fine. This is an actual task. This is just remembering. Oh, this is rubbish. I delete that.
- Me: I like the reminders thing. I think that's to. To add that on because there's a difference between tasks and reminders, isn't.
- Them: Yeah, let me show you. Because we keep showing me all the time.
- Me: There.
- Them: I want to. I want to show up. I want to show off a bit, if I can. Let me see this response because I haven't serviced down, okay? Let me get rid of the Ultra thing.
- Me: I think this is one of the things that I'm finding is I wouldn't. I couldn't sell this. At the moment, it's far too flaky to sell, you know. I mean, the number of errors it makes is quite extraordinary, especially on data. You've got to really watch it, you know, because. Oh, I didn't know you meant that. I'd just be working this for two fucking hours. What do you think I meant? I actually scroll down here as well, and it swears back at you when you. When you say to you really fucked up, that, yes, I really fucked up there.
- Them: Yeah, well, yeah.
- Me: Well. I ran. I ran one of Mike's skills and that said bollocks in it. I think. You know, that's Mike. That is. That really is. A nice one is slash client. Where you. If you're. If you move between clients, you kick up a new terminal and just do slash clients and then the name of the client and it loads the client up for you, so there's no ambiguity about what you're working on.
- Them: Oh, yeah, I see. Yeah. Let me show you just to show up a bit. I know as impressive yours. But these dashboards and this Diabo just goes through all. But then I can select all the clients. These are Clients are really so I have. I don't know. So Shad. That's why I have reminders and tasks.
- Me: Brilliant.
- Them: So this task is in sync with my Google Sheet task, which I share with the client.
- Me: Okay? Yeah.
- Them: Because the client is checks in I don't know. So 8 inch they make I sync that with the Google sheet and the Google actually that can open and change and this this section here, this graph hub is thinking the starts with what I call in the.
- Me: Yeah.
- Them: In the Google sheet and these are reminders. And this is what is being fed from meeting notes from an emails. So I get, so I don't know, I got an email. I don't know if I have any. That need to approve. I may not have any to approve, but it basically will tell me. Look, this is a reminder, so I need to perform this client.
- Me: Yep.
- Them: I need to repair the plan for February March testing period. These are some nodes taken from my call yesterday. Some of them are duplicated. Maybe, but anyway gives me an idea and have the tasks. Fit as well, and I can go and obviously make timeline. And. And. And they have even had templates. Okay. I need to prepare a reminder kind of a task. For promos. So give me. So just give me all the steps. I just add the name, the date. Fine. Create workflow.
- Me: Oh, I love that.
- Them: I don't know. Window sale, for example. 20, 25, I guess. I don't know. With the sale. Gentle sales. So say, okay, fine. This is going to launch on, I don't know, it's going to be on the time unboxing day. Fine. So clear the workflow, and then based on that, I have this. Check the dates. Okay, fine. This is actually going to be, by the way, give me approximate dates and then. Label, and then I kind of blow for high DP because some of these steps will develop for some Granola. Anyway, it's just me having fun. Do I need this now? Make my life easier?
- Me: Brilliant.
- Them: Yes. Was it fun?
- Me: Yeah. Yeah, I feel that matters, isn't it?
- Them: A lot, you know? Daily briefs so I can send okay I missed nearly forgiven because my PC was switched off so I sent daily brief and it would tell me the meeting the clay might things have a day priorities reminders available for the day and for the week or prioritizing a really nice way as a slack message because I'M trying to get everything into slack.
- Me: Yeah. I think, yeah, it's having that single point of communication beyond email, because I've got WhatsApp and I've got teams.
- Them: Yeah.
- Me: The only way I can do that is literally to select all and paste it.
- Them: Yeah.
- Me: That's the only way I can get it in. And it is so annoying. If the client doesn't use slack, I don't know how I can force them to do it.
- Them: Yeah. Had a client who. Anyway, yes, you're right. I have also some dashboards. Have a health dashboard.
- Me: Okay?
- Them: Which, okay. Well, sorry, I don't know. It's not working now. How to use it for a few days. This is basically telling the state of the caches, the email cache and so on.
- Me: Right. Yeah.
- Them: And then I'm working on. Okay. I haven't used it for the. I was working on engaged engagement score. So the idea is, look, there's some clients who are. You know, I just forget about them because.
- Me: You're right. Yeah. You're right. Yeah. It's a great one.
- Them: This is kind of a score, a dashboard that will tell me, look, this client, I don't know, this is gold, silver, bronze. I have to reach 60 points every week and 60 points if I have a call. That's 30 points every email. I said every Slack. Let's check. SM is 5 points if I unless there could be some. It counts the number of changes in the Google Ads. So if I make every. Every change in Google Ads I make is 3 points, and it just scores every week and I reach it and it's. It's kind of gamifying just to make.
- Me: You've done nothing. On it. Yeah. Yeah, that's very good. And do you. Do you feed into that how much they're paying?
- Them: Sure.
- Me: As a proportion of how much money you're right.
- Them: Yes, yes.
- Me: To keep it, isn't it?
- Them: I think. Well, yes and no. That was one of the inputs. But I feel uncomfortable about that because I don't know. How things will evolve. So I just say it's high, low, medium priority, but essentially the same but. Yeah, and there's some but in terms of demand as well. So this is a very demanding client. So the 60 point goal level for some. For some is 60. For some it's 80 or 90, depending on how much they pay, how demanding they are. Because some guy is, you know, they're just happy to get a monthly update, and that's about it.
- Me: Yeah, yeah.
- Them: The weekly call. Some others will have checking badges weekly. So I'm still building it, but the idea is, look, I just go in and say, okay, every. You know, these are in good shape. I didn't speak into them. I think hundred calls with them, communicating with them, doing, doing work on Google Ads at this point is just number of changes. I don't know. It could be hitting weekly budgets and so on. And it tells me, look, these are in the red zone because you haven't spoken to them in all week. You get it?
- Me: Yeah. It's. It's almost like you're saying if you went on the phone call with a client now, how embarrassed would you be? You know?
- Them: Well, only get there, probably, you know, find my way around it.
- Me: Yeah. Yeah.
- Them: I suppose so. I. I would say no, but that's probably going to be a lot of some of that. But, yeah, there is some of that sometimes. But. But yeah, that's about it. It's kind of making it fun. So it's more finding, finding the incentive to go into that account. No one cares about, not even themselves. Because I thought some of the accounts I enjoy the most is those clients are really active. You know, they email me. They're not demanding, but they are people and generally interested to making things work.
- Me: Yeah. Yeah.
- Them: For them and for me and for the business. So, okay. Can we do this? I'm trying this and that, but some others, you ask them something. Oh, yeah, fine. And then nothing. For. For days, for weeks, you can be reminding them nothing. So those. I tend to neglect them. You know, they. They pay. They don't complain. Well, don't complain that you go to a call and they. Anyway, it doesn't matter. So, yeah, it's kind of making it fun to me to find other reason to go into that and work for them, because otherwise. Just forget about them.
- Me: Y. Eah. Yes. Yeah. You do? Yeah. No, I think that's brilliant. I. I have a. I have a client. It's slightly off topic, but they do a kids toy. I think I've spoken to you about them before. And I, he. He's been. We've been. I've been working out strategy to increase budgets and change target roas and so on. And over Christmas, it just goes nuts. And they always run out of stock because it just gets out of hand. I know. I looked at it the other day and you know when you just look at numbers and you don't really go, Yeah, I'm not looking at that as actual pounds. I'm just looking at that as a number. And I've got to increase, decrease, whatever. And I looked at it the other day. Because I wanted one of these toys for my nieces. Son. So I emailed him and I said, it is the only chance, you know, you. You could do me a deal on one of these. And I looked at what his Q4 sales were in the US since October. It was $9 million. And I looked at how much I charge him. And what and when. If he doesn't give me this for nothing, I'm going to go absolutely nuts. Thankfully, he emailed back very, very quick. Oh, yes, you can have whatever color you like. You know, I get it straight away, blah, blah. And I'm looking and going, yeah, you will, won't you? But it was funny how it's like that engagement thing. For the rest of the year, I won't hear from him. And then the Q4. That's when it's all going to go absolutely nuts. But all that preparation for. For the rest of the year has produced those figures now. So it's one of the best success stories, that. But actually doing budget changes because one minute he'll say, I we're running out of stock. Slow it down. Next minute I say, we found some stocks, so can you increase it? And I'm just going in and just saying, saying, read the email. Come up with an email back to him. It's about an A4 page long. This email. Send it off to him. The action, the changes and documents it. So send another email, say, I've just done this. And that's one of the nicest because I, I, it's funny looking at your, your dashboard, I look at it go, that looks really polished. That, that's a really nice way to do it. I've been more textual based than anything else. I'm working in within the system, within Cursor rather than building metas. Manager is outside Cursor. I put it onto a browser, but everything else has been text based. And I'm just running it straight from text. Eventually I'm going to have enough stuff in there to be able to go, okay. Let's gather all this information together. And do a planning session one day to say, let's try and create a dashboard that grabs all this stuff together, and it makes sure I have a universal approach. It's only been recently I've said I've realized that the skills I'm creating weren't universal skills. I've been working on a client and saying I want to do this. And they say, right, well, I've done that. Then go to another client and say, right, can you do this? Why? I don't have that skill. And you go, oh, Christ, no. It's not actually universal skill I've created. So. Okay. We'll go and look in. Go and look in such and such. About this. The skill in there or it'll go and find it. He said there's a skill in such and such a client. Do you want me to use that one? Well, yeah, I do, but I also want it to be universal skill. And it was that structuring of the directory. That you look at you looking at that on a regular basis and going, hang on, he's not writing. And like doing tidy ups. All like the tasks I don't use. I use Google Tasks very infrequently now. Mainly it's just the system task list that I use, but it was saving them in different places. It wasn't saving the task. JSON in the same place all the time. So I got it to tidy all that up and then it the next time you go see, I can't find the tasks. And another skill. Was referring somewhere else for the task. So it's that. It's making sure everything works together. It's been quite complicated. And all it took was the right prompt. And you go, yeah, yeah, I can do that. Yeah, yeah, no problem. Why don't you just ask me? You know? Yeah. And you think, oh, God. So then going back through it. So I think that's why I like terminal, is to go back and go, well, why is that there? That shouldn't be there. And then it starts to unearth other things, doesn't it? So I think eventually, once Christmas is over and I've got some time, I think I would like to do some sort of dashboard and then I can say, well, I don't have to go and do client, blah, blah, blah, it will just go and do that in the background.
- Them: Yeah. Let me, because I spend days fighting for this. The reason I moved from having a web UI to going back into cloth was because I cannot use scales. From the web ui, so those skills are not available to the API. There is a cloud. I ask a question to Mike, which is in the, in the. In the app, in the 1820 app. Passing up on actually got really confused with my questions, I think. But the point is that I struggle with that because I was very keen on using a web ui, as I showed you the other day.
- Me: Oh, really? Yeah. Yeah.
- Them: How to abandon that, give up on that. And go back into the. Not the terminal, but kind of the black screen. Because I could not use the skills. And it's fine. I mean, it's no big deal. Actually, I find it fine. But that was big deal for me.
- Me: Then, wouldn't you? Rather than use the skills you'd have to build a proper app. Because you could use them. You could use like light railway or. Or, you know, a lot of it is flask cap, isn't it?
- Them: I don't know. I mean. There was no. Okay, I'm maybe not inside your question. There was no way available. That I could find. I asked. I mean, I went through everything and I asked. God, I asked. Anyway, there was no way available it will be to invoke, kind of invoke the skills I had in my app.
- Me: Right. Oh, I see.
- Them: Through the API, because the API connects directly to, I guess, the cloud API. And that that didn't make the skill available because it's sitting in my app.
- Me: Okay? And this is funny because we get to this sort of. This sort of stage, it is beyond my knowledge. Sometimes in the way it works. It's like the Railway app. You're using that very simple example of the. Of taking the picture of the. The. The recipe cards. I know I can't do that on my own website, so. Got me, like, you've got the ad success one. I can't create a subdomain on there and just run it on there because it needs. It needs something. It needs Python anywhere is it. It's a. It's. It's. It's the thing that you would put on your own app so you can run Python on your. On your.
- Them: Some driver. I'm going to buy that anyway.
- Me: But it facilitates being able to run Python scripts on there. But then you get into the problem of, yes, the cloud interface. You're going to have to use cloud API, then. Which then starts to invoke cost, which I've done on some of my. Unbeknownst to me, I've. I've been incurring abi costs on there.
- Them: When we use cloud code, we use API costs, so. So I have. Well. I have Cloud Max, and that's for Cloud AI. AI. And that. That is outside the app. That. That's. That's me playing up with some other things.
- Me: Yes. Y.
- Them: And then we have code, and that's linked to the Control API. And those. Yeah, you have to keep putting money into that.
- Me: Ep. But if you've got Claude. If you've got Claude, Max.
- Them: Yes.
- Me: And you're running Claude through your cursor.
- Them: Yeah.
- Me: You're not using any API. There's no additional API costs on that. That's all encompassed within your Claude Max.
- Them: Okay, I'm missing that.
- Me: Yeah.
- Them: That's not.
- Me: You have an allowance in your Claude. Max.
- Them: Sorry. Let me. Let me share my screen. So I have. So. There is. This is claude. Okay? And I have max plan. Okay? And the campaign, whatever. And then this is one, and the other one I've got is entropic. And let us see. Because I was getting. Yeah. So, yeah, I have entropic API, and this is. This is what I'm using and extending. So I have spent two hours in the last week, so I've not really. But the point is, I'm buying credits.
- Me: Yep.
- Them: I mean.
- Me: Yeah, I. I do as well. There's only certain things within your brain. That actually uses those credits, and it is the ones that are running independently.
- Them: Okay? I don't know.
- Me: If you're running like a, a launch agent or something like that, that's running without cursor, without you interacting via cursor, it will use those, those API calls. And this is why you need to look at your launch agent and make sure you're using HeyQ, the cheap one. When you use a lot of Claude.
- Them: Yeah. Yeah.
- Me: If you're using the Opus 4, Opus 4.5, it eats those quite quickly. But ask the question. Of claude. When do I use? When am I incorrect incurring API costs considering I already have a claw max and it will reveal quite a lot of things to you because I had this conversation with it. The other day. And it. It revealed a lot because it'll say, well, this is where you're incurring those costs. These are the agents they're incurring. Do you need to use this level of Claude, Claud? The Claude model to do this? And some instances you can pull it back even further. But $2 is neither in or there is it.
- Them: Yeah.
- Me: That's why it's not going up quickly, because your Claude Max account has been used within. Within your cursor.
- Them: Spending. I don't know how we know how. How does it do it? Because I have added my entropic API. My entropy key. API key. Sorry. The topic API keys. I haven't given it any clue. AI key. So how would it know that?
- Me: Wasn't there a no author similar to an oauth right at the very beginning?
- Them: Yeah, but I thought. Okay, okay, it's easy. Sometime now. So I have. And I'm still showing that we have this file code. This is the one I gave it. Key for testing. I'm not using that. But there is nothing. Include AI, which is the one I'm showing you now. There's nothing.
- Me: I don't know. I. I genuinely don't know how it connects, but it knows you've got a. A Claude Max account.
- Them: Okay, fine.
- Me: We must have done it at some time when we set the whole thing up. Like whether it. Whether. Whether it's in. Because it's probably in. In cursor, isn't it? Within cursor. You're telling it you've got an account?
- Them: To be frank. Why not to be found? I'm trying all the time. I'm finding very frustrating. The conversations I'm having with. I mean, well, that's not true because my lack of vision was useful. But anyway, I find a call is not always really clear about. APIs and keys while using this of that. But not. Not. But I'm not being. I don't. I remember not because my Dasco. I mean, there was a time. There was one day when it got. Because I. I remember when it had my last. My late. My last call with you. I felt a bit frustrated. About how things were going. I was getting all these talking issues and so on. And.
- Me: This terminology. A lot of it, isn't it? A lot of it is terminology because it's new terminology to us.
- Them: Yeah, but there was. There was something, anyway. I. I got past that point. I think I. I was able to trust I understood thing about tokens, I got more relaxed and because I understood the context stock in his 200,000 as opposed to 12,000.
- Me: Yeah. It's so annoying when it compacts as well. That's really, really frustrating.
- Them: He was really confused the way and I was getting some Airbnb anyway. You know, I just got past that point. And I obviously understood. I kind of used the skills. Within the web ui. So I moved away from the UI and I kind of simplified things. I made more confident and anyway,
- Me: Y. It's a proper tool, though, isn't it? It is a proper tool. It helps us with our job. I say, you couldn't necessarily give this to someone, say, go and use that, then you can go and do it. It's not like that at all, and that's what I love about it. That it is. You know, you're downloading from your head. Stuff like. Like the landing page. It just go go look back through my emails. I can't remember when the landing page test started. Anyway went and found it. And you just go, God, I never remember that. You know, and it's just joining the dots with all that. And, like, creating monthly reports. What have I done during the month for this client? I have no idea. What were the results of what I've done? Well, there you go. It's. It just. It just does. It. It's that completeness that. It's really quite scary, but I'm. I'm. I'm absolutely. As much as your grin tells me, I'm really enjoying it as much as you are.
- Them: So really to me when we are in a situation now do you have a hard stop now or you can find so I'm not going to take all the time.
- Me: Yeah. No, no, no.
- Them: I want to go and take a nap. I don't recall this morning. I did a presentation, so I'm really tired, but anyway.
- Me: I just cancel my call at 2:00 and I can't be doing with this.
- Them: No, no, no. I was looking forward to it.
- Me: No, no. I just canceled my call at 2:00. Yeah, I didn't know. I did it early on this morning. I just. I didn't have the capacity today. I've had to take my sister to the hospital this morning for an appointment, and it's just. It's been full on all day. The last thing I wanted to do was speak to a client. This has been a good relief, I think.
- Them: Okay, Fine. Sorry. Finally. Go well, we'll catch up another time. And. And go into some of the things as well.
- Me: Yeah, absolutely. Yeah, I'm. I'm happy to do this every week. It's the voyage of discovery, and no one else understands what the hell I'm talking about.
- Them: Let's do something. Okay, fine. If you you're happy to do wakeling, can we. I mean, does is this time work for you? Quickly?
- Me: Yeah. Yeah. Yeah. Yeah.
- Them: Yeah. So wonderful.
- Me: It's. There will be some Fridays I can't do. Sometimes we go away for the weekend. But it's not. There's. There's nothing in the near future. We can always move it around, can't we? Let's just put a line in there. And then we can move if we need to.
- Them: We done? We can skip from time to time. We're going to get bored of each other, so. Yeah, we can. Yeah, that's fine. Okay, I'll make it. I'll make it regular. Well, not every week, anyway. Yeah, with a few exceptions. I will make it regular. So, you know, we can always escape if it doesn't work or we have lots of things.
- Me: Well, it's. It's good. It's good to talk about this because, you know, all of you just come up with ideas, don't you? And you only really realize them. I've recorded it again. Like, I've stuck this on Granola. I literally do it for everything now. And even that, it's amazing what it pops up with.
- Them: Pretty addictive. Anyway, but just go. And again, I've heard there's somebody from, from a previous call with a client and I, I just got. And the summary starts for good. And again, we're always scratching the surface because this templates, these recipes and all these things with Granola make. When I say circulars, we're probably getting 70% of the value anyway. But this. There's more that. Anyway, I mean, just that. Just the basics is. Is plenty.
- Me: And that's all I use, because I'm just using the raw data. I'm just using Granola as a way to gather the data, put it into the Google Doc, which you told me about, using Zapier. And then put it into. Into the system. Fantastic. That's a great way to do it.
- Them: Did you send? Do you give cloth? All the trans. All veterans. All the transcript or the notes from Granola?
- Me: Yeah, all of it.
- Them: Because, I mean, I only did it. I'm always thinking of tokens, which just. I think I. I got traumatized with tokens that first week, and I can stop myself. But. But the summaries are really so good. But yeah, I mean, transcripts. I mean, you have calls that can take go like this one, right? By the way, that's fine. I got footnotes. But I can always provide the transcripts if needed.
- Me: Yeah.
- Them: But I'm just thinking if I'm missing out something. But I find the note so good that I don't really. I don't know, I may be going. The transcripts may be good for kind of exploratory calls with new clients, but the regular calls. Sorry, I'm just thinking. Out loud.
- Me: No, no, it's fine. No, you're right, because there may be some nuance in there that you're missing, or there may be some detail that the summary is not actually capturing. And you could always go back on there and ask, you know, did the client ever mention this? Well, that might not be in the summary.
- Them: I found myself going to Granola about a couple of things. So I wasn't sure about the dates of a promo. I went into Granola and asked, what were the dates of the promo? And Granola is great. I mean, they may be using gold code in the back end. And it gave me the perfect answers. Now I could have get the trusted in through clothes and then ask the question to close and probably that would be better because then I have all the information I need there.
- Me: And I don't want to go anywhere. I don't want to go to multiple places. I think that's the thing. I don't want to be going to all these different places to get data. I just want to go to Claude and say, go and get me the data, wherever it is. Did we ever talk about this with such and such a client? Well, it could have been a teams meeting. It could have been a Granola import. It could be in an email. I don't want to have to go to three different places. Just want to go to one and say, give me all the details about this. It's ever been discussed. And it's just so annoying with teams just having to cut and paste. Bang. But remembering to do that, I'm setting a task to do it. You know, so that every. I've got recurring tasks every seven days or something. It'll pop up. And I say, all right, I need to do that. And then because the task. If I say completed, carry out this task. Save. Put that into process. My notes. I put that into Claude and it goes and reads. So what's happening in task is when you. When you take my notes. It copies that into downloads folder. Then I go to Claudia. If I say process my notes, it will read that download folder. And then go and do whatever I've asked it to do within the. Within the task. But everything's visible in the task. I think that's the nice flow of all that, that you don't need to remember the detail, that you've already saved it within the task. And you don't need to know what to say to Claude, because it's already in attack what you. What you want to achieve from it. So it's. Yeah, it's just a. It's just a nice kind of flow to it all. And certainly it's all done within. Within Claude as well. It's proper techie, though, isn't it? I feel a proper geek. Really do feel like a geek. It's great.
- Them: I'm thinking, what next? I'm thinking, okay, this is Google Ads, but what next?
- Me: Yeah.
- Them: I'm thinking about other projects because, as I said, everything is possible now. So all the things I thought of doing that it felt, well, you know, I'm not going to have two years to build this. I can build in two weeks.
- Me: Yeah, yeah. Yeah. I tell you one thing to be very careful of. If you go down the Microsoft ads mcp. That is a bitch. As ever, Microsoft ads is a pain in the ass. You've got to use an Azure Cloud account to do it. I was on the phone. For pretty much two hours with Microsoft trying to sort it out. It was just a nightmare to the extent where I've set it up, the necessary links and so on. I've not even touched it since. It just sucked the lifeblood out of me. And you think, well, I don't. I don't really. I'm not up to date with Microsoft ads as much as I am with Google Ads, so maybe it'd be a good thing with code to use it to. To optimize things. I can't be asked. You know, the amount of money it generates. I cannot be bothered at all. It's the usual thing. What do I do? Do I spend an hour on Microsoft ads or an hour on Google? It's a no brainer, isn't it? You know, I'd rather spend an hour doing bloody recipe cards than being on my consultants.
- Them: Here. It's getting worse. So destroying going through the amount of Microsoft ads a ui. It's just like what I'm doing Megaway.
- Me: Yeah. Yeah, yeah, yeah, you're right, you're right.
- Them: Anyway. Well, have a good weekend.
- Me: Lovely. Yes. Enjoy that. Thank you, sue.
- Them: Take care.
- Me: Have a good mate. Bye bye now.

## Transcript

--- Enhanced Notes ---
### Current Claude/AI Development Excitement

- Both feeling transported back 15-20 years to early programming days
- Similar excitement to when Sergi started with Google Ads in 2005
- Peter feels like he’s rediscovered the joy of coding
- Everything feels possible now with modern web development technologies
- Node.js, Express Server, Flask apps
- Cloud deployment via Railway for web server hosting

### Peter’s Recipe Card Project

- Built system to digitize Gusto meal kit recipe cards
- Takes photos of front/back of cards
- Extracts text automatically into searchable format
- Kids can search by ingredients (e.g., “courgette and chicken”)
- Demonstrates rapid development capability - completed in \~30 minutes
- Planning web deployment via Railway cloud platform

### Development Workflow Preferences

- Peter uses raw terminal screen with Claude
- Prefers text-based interface over formatted chat
- Uses bypass permissions flag to avoid constant prompts
- Often runs 2-3 hour development sessions
- Sergi primarily uses chat interface
- Finds prompts manageable for smaller batches
- Typically works in 5-minute increments

### Peter’s Advanced AI Knowledge Base System

- Building comprehensive brain dump system
- Pulls from Google dev blog, industry experts (Brad Geddes, Frederick Vallaeys)
- Updates weekly, monthly, quarterly, yearly
- Indexes content properly using SQLite
- Strategic decision support
- Analyzes context for Google Ads optimization decisions
- Suggests alternatives based on knowledge base
- Acts like having an apprentice
- Integration with Google Ads management
- Writes strategy reports and client communications
- Implements changes directly via API
- Includes mandatory validation protocols (backup, dry run, verify, restore)

### Advanced Google Ads Automation

- Asset text optimization system
- Pulls headlines/descriptions from PMAX campaigns
- Analyzes 90-day performance (CTR focus)
- Categorizes underperforming assets
- Generates 15 alternative text options with dropdown selection
- Experiment tracking system
- Logs all changes with expectations
- Creates follow-up tasks for 4-week reviews
- Provides categorical success/failure analysis
- Client example: $9 million Q4 US sales for toy client
- Handles rapid budget changes during peak season
- Automates email responses and change documentation

### Sergi’s Productivity Systems

- Live audit system
- Reduces audit time from 6-7 hours to 30 minutes
- Built from scratch rather than using existing templates
- Meeting preparation automation
- Pulls from Slack, emails, meeting notes
- Generates formatted Google Slides with client logos
- 10-minute prep vs 2-3 hours manual work
- Automated reminder system
- Scans communications every couple hours
- Sends Slack notifications for tasks/reminders
- Integrates with custom dashboard for approval/deletion

### Dashboard and Task Management

- Sergi’s comprehensive client dashboard
- Task management synced with Google Sheets
- Client engagement scoring system (60-90 points weekly)
- Health monitoring for caches and systems
- Engagement gamification
- Points for calls (30), emails (varies), Slack messages (5), Google Ads changes (3)
- Adjustable targets based on client payment/demands
- Red zone alerts for neglected accounts
- Template workflows for recurring tasks (promos, sales periods)

### Technical Integration Challenges

- MCP server implementations
- Shopify integration working (requires app setup)
- WooCommerce integration functional
- Google Trends problematic (timeouts, API limits)
- API cost management
- Claude Max covers cursor usage
- Separate Anthropic API costs for independent agents
- Recommendation to use Haiku for cost efficiency
- Skills vs API limitations
- Web UI cannot access cursor skills
- Forced return to terminal interface for full functionality

---

Chat with meeting transcript: [https://notes.granola.ai/t/86d253a0-72f5-4a7a-bb96-87e3237ba898](https://notes.granola.ai/t/86d253a0-72f5-4a7a-bb96-87e3237ba898)

--- Full Transcript ---

Me: Hey, segi.
Them: Hi, peter. Hello.
Me: Yeah. Good.
Them: Yeah. Good.
Me: I've got. It's Friday, I must say.
Them: Yeah, well.
Me: So tired.
Them: How's it going?
Me: I feel like I've been transported back about. 20 years, 25 years back to being a programmer. And being excited about code, and so I've not been able to walk away from your desk.
Them: Look, I didn't say 25. I was thinking 15.
Me: Oh, okay. Thank you very much for that. I appreciate that.
Them: Thousand. Well, I'll get. Fine. Didn't sound the way it went, but anyway, I thought exactly the same. I thought exactly the same. Right. I was thinking about it just 10 minutes ago. I was thinking, how do I feel about this? And I was thinking, it feels like the self excitement I had. Well, I say 15, but actually now it's more 20, because 15 is when I got into Google Ads. Yeah, that's the sort of thing I got back 2005. When I. I started playing up with java. And, you know, and all these things, you know, getting deep into programming, and that was actually.
Me: When you've enjoyed it. When you enjoy doing it as well. That's the thing that gave me the buzz.
Them: Yeah, yeah, yeah, yeah.
Me: I'm glad you feel the same. That's brilliant.
Them: Exactly, exactly the same. And. And actually thinking back, so before starting at Success, that was obviously on my own, doing work for five, six, six clients. I was thinking. Look, this is not going anywhere. I'm not really loving it. I know. You spend four very intense months. Learning about Node Lending, about Express Server. So all these web development technologies that have been, you know, created, that were new. That didn't exist. When I was building, you know, from its clothes, so to speak. 15, 20 years ago. So now, obviously, everything has changed now.
Me: Yeah.
Them: And everything is possible now.
Me: Absolutely right. Absolutely right. Everything is possible. That's a really good way to describe it. It's really strange. Isn't it? I'm using. What's a flask app? I have no idea. I don't know what railway is. Railways to run an app on it on a web server. So you can run a cloud app on a web server and access it anywhere. Yeah.
Them: Do you think my way? I started using my weight yesterday. Yeah, yeah.
Me: So. And it was a crazy thing. I said, we have. It's got to be called gusto. I don't know whether you were aware of it in the UK when you were in the UK with you had it or not, but basically they provide the menus and the ingredients. For meals. So you say, right? I want to buy four meals. I want this one, this one, this one and this one. They send you the fresh vegetables and all the rest in a box. With all the meat. All the rest of them come with four cards. If you got four recipes and you follow the recipe on it. And it's fabulous food, absolute, like, techniques you wouldn't normally use. It's not cheap, but it's really good with eating some fantastic stuff, even though it's a good cook. Anyway, it's different stuff. So I thought, okay. What if I took a pitcher of the front and the back of that card? Made it into a recipe and then put it on the web and made it searchable. And then the kids could access all those recipes. So you could say I've got courgette and chicken. What have you got with courgette and chicken? In and it would go and pop up the recipes. Yeah, done that. So actually taking a photo of it front and back, it reads it, it puts it into the right sort of floor mat and it puts it onto the Internet. I've not got the Internet bit yet because I've not got the railway bit, but that was like half an hour.
Them: Sorry. Are we talking about pushing recipes? Sorry I lost you there. I thought it was. It was as it was an example. And then I realized you were talking about real thing.
Me: Yeah. It was a real thing. Yeah. So we got these cards, these recipe cards. That from Gusto, I thought, take a picture the front and back of them. And there's photos on there, there's all sorts, but I just wanted to get the text of it. And they're in the same format. It's got the nutrition on there. It serves this many. And then it's got the actual process, but it's got a list of all the ingredients. Above it. So I'm going to put that onto a web server. So that the kids can go onto that web server, given the password, and they can go look for these recipes.
Them: Okay?
Me: So they're all searchable. And it was just a bit of fun. And this is like you got your four things running. You think, well, I've got a spare one there, let's do it on there.
Them: Yeah, he's like a waste if you like. I mean, you have three screens, so why not have three things building at the same time? I have all this chat tabs and I have two, three working at the same time. I sometimes think, well, why don't I have a fourth one? And I'm building something else.
Me: Something for a bit of fun, yeah?
Them: Right. For fun. For fun.
Me: Now, the interesting bit is, okay, so actual technique there. Do you use terminal? Do you use chat? On cursor.
Them: I mostly chat. Very rarely I need to use terminal.
Me: So I use the raw terminal screen. I'll just type Claude into when it pops up. Type Claude in it, does it? It's not. It's the pure text version. There is the chat version, isn't there? Which is a little bit more formatted. I don't actually use that anymore.
Them: Sorry. By the way, this one? I said five. Okay, go ahead. Here.
Me: So if you call it terminal, in chat, in cursor. So the one thing I've done is I started up doing Claude. So I just run claws and it pops up and you can go and use Claude in it. So then I've done. What Mike's done is using the abbreviations. And done the version where. What's the name of it? There's the flag which says ignore any sort of input at all. Just run it. And it just blasts its way. I can't remember what it's called now.
Them: Composite.
Me: No. Damn it. What was it? I'm normally talking into this. It's weird typing. Because normally it'll prompt you, wouldn't it? It said, do you want to use Bash? Do you want to do this? So you can actually set the flag that just goes. And it just blasts through it.
Them: This is not what you explained the other day. How did you call it?
Me: 's a really weird.
Them: Can you tell? Very composer.
Me: No. It's a flag to use with Claude. When I find it, I'll let you know.
Them: You asked for a feature or something, you enter the prompt and what would normally happen is that it would ask you confirmation to things.
Me: Correct.
Them: Sometimes you get yes. No. Sometimes you get yes. Sometimes you get yes to everything like that.
Me: Yeah. One, two or three? Two. And one and. Yeah. Make sure you're awake. Yes.
Them: I normally go at some point. Maybe the first part, they say yes. And the second one, when I know it's going in the right direction, I go yes to everything. And then I move on. I come back five minutes later.
Me: Yeah, there's another. There's another version of Claude where you can run it with a flag. And basically you just leave it. You say, I want to do this, this, this, this and this. And it goes. And it just rattles it off. And there's very few prompts. You got to be careful with it. It's actually doing the right thing.
Them: Okay? Yeah, I. Don't find I don't find the prompts, I don't find I get too many problems. I don't think I'm being delayed. I mean, it's not like. Look, we have to build this today point, okay? The client is like, okay, fine.
Me: Yeah.
Them: If I get. Look, I don't think we'll make. I mean, if I'm the scientist correctly, I don't find it particularly annoying that I get prompts from time to time. And when I get the option, normally just go for yes to everything and it leaves me alone. And to be honest, I work in a small batches, so it's not like I want. I mean, I don't expect to add a prompt. I will require an hour's work. For Claude. Normally within five minutes.
Me: Oh, gosh, I've been to two or three hours.
Them: The time.
Me: Just on one thing. When I'm planning something, I'll just put two or three hours. It'll just go and do it.
Them: Okay? Okay, let's go. Okay, let's go. Where are you building that will require two, three hours of work every day.
Me: I'm building my brain, Sergey. That's what I'm doing. I'm building my brain. Okay?
Them: I wish you.
Me: I'll give you an example. I'll give you an example. So I've got a knowledge base. Right. I'm at a stage now where Mike produces something in his brain. And I'll pull it in and I'll say, what's in Mike's brain that I could put into mine. And I've got to the point now. He said nothing. Yeah. There's nothing that you can do. There's nothing you can add from Mike's brain to yours where he's doing it better. Because the thing with Mike is. And that's not an ego thing. He isn't running an agency. A lot of the stuff he does isn't agency stuff. And when he goes and does the CSV analyzer is very good. I really like that one. That is very good. But most of the other stuff, like where he's doing the search terms, I'll put it into high and medium, low intent. You just go, yeah. 20 and it's got tired. It couldn't do anymore. Well, I've got 100,000 in there. What am I supposed to do with those? How am I supposed to categorize those? If you want to do over a big period of time and make it worth your while. So I don't tend to do touches. But one thing I did do at the beginning was I wanted a knowledge base. The key to their brain is that we are doing a brain dump. We're actually saying, these are all the things that I know. These are all the things that the Internet knows about what I know, what I do. I want to put them all into a knowledge base. And I want to keep that up to date. I want to be looking at the Google dev blog on a regular basis, see if there's anything on there that's interesting that I might find interesting and bring it in. It's something Brad Geddes is doing that's interesting. Frederick Valets what they talk about search engine life, all those. So I started doing that, and I pulled in. I said, go and find me some websites with Providence and people with Providence and pull it all into a database. Mike then was talking about his brain was talking about using SQ Light for doing indexing. So it will actually index it properly. And then I took it at stage further. The other day. It's like taking a stronger and stronger drug, isn't it? You just push it a little bit more. So now the knowledge base will update every week, every month, every quarter and every year. And it will basically mash it all together, all the stuff that's being talked about. And I can either search it and say, what's the latest thinkings on pmax optimization? Or I've got it now and I'm still not sure how it's going to work this because we literally finished yesterday. But when I make a decision, a strategic decision in Google Ads to say, I'm going to do this on this client, it will then go look at the knowledge base and say, I've got this context about that. And maybe you want to try this or maybe you want to try that. That's what I'm aiming towards. But it's like having all of it is like having an apprentice. And you say, can you go and do that? And you go and give it some work to do. And it comes back and you read it and go. And I've said it to before, that's rubbish. That's absolutely rubbish. Because of this, this and this. You're absolutely right. I'm fed up with it saying that, but you're absolutely right. I didn't do this. Or I didn't do that. I'd done a report for a client and it was completely wrong. And he said, well, I didn't really wanted the latest data. What do you mean? Well, yeah. Then you build stuff in like that. I'm now using it. So you said the top five, but they're all kind of blended together. But I got it to a point now where I'm writing stuff back to Google. So I've got a client now where there's some big budget changes, so I've done a Q4 strategy report for it. And then said, give me that strategy. Let's go and look at it. We find all the strategy when the budget changes need to be based upon last year's conversion rate increase and decrease because of Black Friday, Christmas and all the rest of it. And then I'll say, do a report. Write the email to the client, write me a team's message to the client, formatted nicely and then affect the change. So I was prompted by Mike saying about hooks, actually putting a hook into it. So whenever this happens, always do this. So I'm thinking, okay, what I actually want to do is when I make a change, And to get it ready to send through to Google. I want. It to back it up. Back up the existing position for whatever it's looking at. Do a validation of the data that's going in prior to it going in. Make a run, a dry run, make sure it works, then do the live run. And then verify that what you asked it to do. Has, but then always have a restore position. It didn't actually work the other day, the restore, but that's a different story. So I was doing that as a hook. I think every time you try and change from Google Ads, do this process, it doesn't actually work. It won't do it on an API, a hook. But now I've built it into my context. MD that this is a protocol, a mandatory protocol at the top. Do this, this and this. It's brilliant. Eden's the point where if you're in this super duper mode where it's just blasting through, it would stop and say, I'm going to do this now. Are you all right with this type? Yes. To continue. So you can read what it's saying. Type. Yes. And then it will go and do it. That was a belt of that. That was. I really like that one. But I'm doing more and more of that writing stuff back into Google Ads, which is quite scary. And I just tend to. Download into Google Ads Editor, do the change. And then download to Google Ads editor where all green bits highlights are and just see what I mean. Change the right thing. I said it's caught it a couple of times, but it's not done what it's supposed to do. But a lot of the time it doesn't re enquire on the Google Ads data through the API. You got to really tell it that I want the latest data. And then it will tootle off and do it. So I'll go on. Your turn.
Them: Yeah, yeah. I've been thinking about things like that, but it's like, I don't know if. I don't know if it's the way I work or is the type of clients I got. Maybe I'm lazy. I don't find very often that I have to do. That much work on the Google Ads account. So it's more about you set up a new campaign, I mean. Just to get stuff, just to say in terms of search campaigns really is just. Outside from brand campaigns. It's only two clients where you really use search. The rest is mostly shopping. Or is it mostly is pretty much all shopping op Max. And then we have a marketing mags. Do we need by hand? It just feels right and I wouldn't be optimizing it. So. What sort of so are you talking about? Maybe, I don't know, your hotels client when you have to create many campaigns and I don't know.
Me: No, not necessarily that. One of my favorite ones at the moment. It's very nearly finished now. This was prompted by a client who's changed all his text outside my control. Changed all the text in his ads, but Black Friday all over it. All over it. Now he wants to revert it back to Christmas, and then he wants to revert it. To. So I said, well, you do that. You change the text. There you go. There's the spreadsheet, a G sheet. With your latest position, with your headlines in your descriptions. You can go in and change that, and I'll suck that in. And that's pmax and rsas.
Them: Okay, so that's you telling Claude, go and take this.
Me: No telling the client, I'm saying. So I've pulled in the latest position as though you were going to do it in Google Ads Editor. But all it says in the sheet is the text assets.
Them: How the height.
Me: I've actually looked to do image assets now as well, so you can change those. They're a bit tricky because their IDS. But download it into a G sheet. So you got one sheet for pmax, one sheet for rsas. He's landed me in the ship because he just got rid of who was effectively my boss. I've never had a boss for many years, but she said she was my boss anyway. So he said, I'll help you out with the text. I'll do it. Right, fine. There it is. There's the sheet. You tell me when you finish, and I'll suck that back into Google Ads. It's been a bitch to do. But off the back of that. I've got something that will pull in. Apmax campaign. The asset text from a PMAX campaign. So headlines, descriptions, long headlines. It will pull it in. It will tell me how they've performed over the last 90 days. So really click through rate and conversion rate. I'm more interested in click through rate than anything else. Then categorize them. Which ones need changing, which ones have gone stale or just aren't working? So it will look at it. As a client base, not just saying, is it less than 5? So look at that asset group. Highest is this lowest is that. Which one should I actually be looking at? It'll bring them back in a list. I just want the high, the high priority ones. So the ones with the very low CTR, and it'll tell me what the CTRs, what the conversion rate, what is the conversion? It will tell me why it says it's a high. It'll tell me what the current text was, and then it has a cell. With a drop down List of 15 alternatives of text that I got clawed to do based upon criteria that I've set for all the clients. So it'll go and look at them, it'll look at the URL. And it will bring me back a selection of different ones. So ones that are technical brands, quirky CTAs. Give me a choice of those. They all keep. Then I can send it back again and it replaces those. Assets. So it's an optimization thing, and it's something that. To do that manually. Once I get it right. It's nearly there. To do that manually would take a long time. It's something I never do. I never, ever do that. I never go and optimize my asset text. And you look at it, it's lying you through. Top 1. Top ctr 8%. Lowest 0.4. Why would you want to keep that one? What a difference that will make.
Them: Well. Okay. My view probably not a lot. Sorry. I'm saying this because I go through these reports quite often and what I see is that for big enough accounts, and that's different story when you're spending £20 a day and we're gonna have the data and there will be wastage there. But for, you know, big enough accounts, you can see the best performing ones, the best performing headlines based on descriptions, the ones that perform, that tend to get the most impressions. But no, you're right. I mean, there is that. And there is also the fact that you have maybe 50% of the headlines that are underperforming. And still spending, you know, some amount. So it's the case of why keeping them there. If you remove them, yeah, it's gonna be small impact, but that's the saving. And maybe that stops you from trying new headlines. So there is some truth in that. But. Yeah, I mean, I always think. The lazy me always think. Look, is it worth the effort if it's gonna move the needle in a meaningful way? And maybe just ask me. You know, just. Okay, that's an excuse.
Me: You fit the nail on the head. So if you've hit the nail on the head there, because you asked the question before, why do it in Claude? Why change it in Claude? And the reason is I've got an experiment system that is logging when they go in. Is creating a task for me to go and looking back in four weeks time to see whether they worked or not. I will know categorically. Whether that has worked. And that's why I'm doing things through Claude. Because I'm logging things. I know we can go into change history, but there's certain things not done in change history. And in change history, you can't say why you're doing this. So the experiment system I've got is it says this is the expectation that you've got. Let's go back, let's set a task, because I've now got a task manager system as well. And prioritizing tasks. And it will pop that up as a priority, so you need to go and test this. And the task manager. When it sets the task, it'll put in it in a great big chunk. This is why you're doing it and this is what you've got to ask. So I go right. Add a note to the task. Save it, put it into Claude and says, process my notes. And he would have dragged all of that into Claude. And he'll say, right now, go and run this. And it will go and process that task. And do the things I want so I don't have to remember it. And there's little, tiny little things. That I've changed. It's working. Is this not working? And you look at it go, no, categorically that's worked, or categorically, that hasn't worked, and you may not have come to the same conclusion. If you've done it manually because it has got all the facts. Not necessarily a snapshot, but you can go back on the API and see what the position was before and look at it now and go, there you go. I think this. What do you think? Now? 50. 50. I'll say. No, I think that's bullshit because you've not done this. You've not done this. But a lot of times you go, oh, that is very good. And it's because you have logged it. In clothes. I'd love to do everything in Claude, I'd look to not touch the dashboard at all the Google Ads, ui. But that's never going to happen for a long time. But it's been really handy. Really handy.
Them: I'm not going that deep into Google Ads at all. At all. I've been. Distracted about when you mention a dashboard you transportation list. I go down that route as well. So I would say probably a lot of my time with Claude.
Me: Great.
Them: Has been a lot, not everything. But what has been on productivity. So, for example, to have few things that build. So in terms of Google Ads, a couple of things I got, I've got, I've created what I call a live audit skill, which I don't know if I was, I don't, I don't know if I use one of mics as a does not as a draft, as a template.
Me: Okay?
Them: And I think I created one from scratch. It has been very helpful because I had a couple of audits reviews for potential new clients. So look.
Me: He has a no.
Them: I'm able to do in 30 minutes. The other day. I just had a presentation this morning. Got a potential new client. Not, not. Not particularly interested in this one. But point is, I did in an hour what normally what it would have taken me otherwise, six, seven hours.
Me: Fantastic. We talked about that, didn't he? That is brilliant. Absolutely brilliant.
Them: Six, seven hours. Yeah, yeah. That was the first attempt. I was building it and going through, so now I've had it. Next time it's going to be a lot easier, not faster.
Me: Did you feed in your existing audits to that, then?
Them: Second. No.
Me: Did you feed? No. Okay.
Them: Yes. And now? Well, obviously, I. My promise included all the things, all the questions, all the knowledge. But no, I did not.
Me: See, that would have been my starting point, I think. No criticism. It's just another way of thinking. But I would have fed in all the audits you've ever done. And say I'd want to create. Go into plan mode and say I want to produce a system that produces what it's like this. Off it goes.
Them: Okay? Maybe.
Me: Have you used Ultrathink yet?
Them: Ult I think.
Me: Ultrathink. Ultra. It's fun because it does it in a rainbow color. When you type in Ultrathink, it comes up with rainbow colors for the latter. So it's worth just to do that.
Them: Is that? Is that. I would say that is that. Is that a cursor in cursor is saying.
Me: Yes. Yeah. Yeah, yeah. If you're running Claude in cursor, in terminal. If you're right, ultrathinky. Or write it. Alternating colors and letters.
Them: So if I. Let me share my screen.
Me: Yeah. Sure.
Them: Sorry. I'm trying to find. Okay. Yeah. Here you go.
Me: If you try Whisper flow out yet.
Them: Yeah, I'm wasting all the time. Make fan. I'm getting used to it. Not in paid mode yet, but I may. Well, I think I will agree soon. And what? What do you want? To show you. Okay, fine. So we are. Sorry. So is that. Did you say ultra? What is it? Is that. Is that.
Me: Ultra. Think.
Them: Is that here? Where would I find it?
Me: I can't see screen.
Them: How you. Oh, sorry. Why not? You cannot see it. I'm not sharing anything now.
Me: No. No.
Them: Okay, let's try again. Now.
Me: Yeah.
Them: Yeah, okay. So what is it?
Me: Just type in ultra thing there.
Them: Ultra thing.
Me: Yeah. No gap, no space. Right. It must be in Terminal then. Can you go into Terminal? Is it Command T or something? That's it. So if you go into Claude there.
Them: This is what you mean.
Me: Yep.
Them: Okay. This is how you're using it.
Me: That's how I use it. Yeah, all time.
Them: Then. Okay?
Me: If you do one.
Them: So, you know, using this chat box.
Me: I use that all the time. I've got four of those going any one time. So if you type in if your query there. And you use the word ultrathink in there. Just type ultrathink. Now, that's the fun bit to start off with. There you go.
Them: So is that it?
Me: But it's really handy because, you know, you could use. You could use Opus Force on it, whatever it might be. Using ultrapync, uses the most powerful model. But you can do it per queries. You're not paying a huge amount of money for it. So if you. If you would. If you wanted to do some analysis, say you wanted to do analyzed Black Friday results for such and such clients. Comparing with last year. Ultrathink. It will take longer to do. It'll do a deeper thinking. Most of my stuff I use Haku. I've got it to default. All the agents and launch. Most of the agents and launch agents use Haku rather than sonnet or Opus 4.5. Because they're more expensive. I know he dropped down every now and again or go up to this. That's a great way to do it.
Them: So you go. You go ultra think and then you type. Then you press enter, I guess.
Me: No, no, no. You just. You just use the word ultra in your.
Them: The question.
Me: Prompt.
Them: Analyze. Analyze search. Intent for client? I don't know. Campaigns for the past 30 days.
Me: Yep.
Them: Is that what? You okay? Fine.
Me: So just. It will take longer to do it.
Them: Okay? So tell me, tell me again. Why is this better than just going through this box? And just, like, asking the same question.
Me: You know what? I don't know. I just prefer it.
Them: Okay, fine. Okay.
Me: I think part of it is because I'm from a Unix background. And I just get really excited seeing UNIX commands. I'm doing IT backup and it says tar. And he's going, bloody hell, tape archive fantastic. I'm old enough to know what it means. It's like grep grab expression. Orc.
Them: The type one is not very. I find it not very responsive. I don't know. But. No, I mean, you're familiar with it, that. That's where you.
Me: Well, let me share my screen with you. I think it's fun to see the way other people work, isn't it? Because we're giving so many different ways to do it.
Them: Oh, wow. I mean. This. Oh, my God. Oh, my God.
Me: That's the way I work. And it's like, as you say, I've got this. Oh, he's still waiting. There, let's hit yes on there.
Them: And of course, of course, this is just one of screen.
Me: Yeah. Well, this is the three sessions I'm doing. If I go up here and just split that. If I do ca. I've got an abbreviation for this. It's got bypass permissions on now. The bottom there. You see that?
Them: Yeah, yeah, yeah.
Me: So that's the bit where it doesn't ask. Like I've got that middle one said yes or no. Sometimes I might want to look at other times I just want to blast it through. I don't want to be interested. But if I do shift and tab on this one now, I can still go to plan mode.
Them: Yeah.
Me: So, you still there?
Them: Yeah.
Me: It's just kicked up another screen because. I've lost reset. You've actually completed there, so keep that with me a minute.
Them: I'm still seeing your terminal.
Me: What on earth this happened? There. I've just lost the. There we go. Does cut it. What was I saying then? Yeah, I can still scroll through these so I can go into plan mode if I wanted to. Shift and tab bypass Shift and tab. Don't know what that one is, but then accept edit on. So if you start it with this flag, you can still flip between all the others. If you wanted to step through it a bit more, you can still use that. Accept add its own. Or if you wanted to do something quick, you can just do bypass permissions on.
Them: Yeah. Yeah, okay.
Me: I do find that really interesting.
Them: Yeah, indeed. I mean, you have tasks going on for hours.
Me: But that's what happened with the. With the. Doing the. The knowledge base one, because it then went off. It found a whole new load of articles to go and do. Had to do a web pool for all them. Sorry, a web fetch. And then stick them all into the database, and then. So I'm just leaving that running. Another really interesting one is doing unit tests. That's one of mics that where you. You say to it run or, or you can do some setup. Unit test or run unit test. Specify unit tests. And the unit tests go into your code. And test it all. And it will toot laugh. This stuff it found I was getting dead locking. I was getting old scopes were wrong. It was. It saved me so much time just using unit tests. And it will just. I say one of these. It'll just run through. It'll just keep running through. And said, so many passed. I'll do them in phases. I think these are important. These are important. These are important. It'll run them and then carry on.
Them: So you need. You need tests. Okay, unit test.
Me: Your project.
Them: Your project, your. Your agents as well, I suppose.
Me: Everything? Yeah, everything. Yeah.
Them: Okay? Because you have staff running all the time, right?
Me: I've launch agents running. Yeah. And they. I've got an agent dashboard now. I got to keep my eye on them because every now and again they'll just bomb out. And I've got one thing I found was because I'm switching my computer off every night, so if I set a schedule, They weren't running, I'd set them for 6:00 in the morning, start at 7. So now there's that flag that says, if they've not run already, then run them. And now I've got another thing that runs. I've got a health, a slash command. So I've got health and it'll run that command, that skill. And it'll just. It'll blast it through. Make sure everything's working. I've got launch agency. It'll just go and start everything.
Them: Yeah.
Me: Seriously, all this stuff about the electricity and cloud servers and AI taking all loads and loads of electricity, it's me. It really is me. I'm just totally addicted to this thing. I think it's fabulous. And this, you know, the most important thing. There's stuff I'm producing for my client is extraordinary. I did. I did a landing page report for a client the other day, and it happened to have failed the landing page report, and it was like that. And I put screenshots in of the landing page before and after and what I was testing and why it had failed and why I thought what we could do in the future. And she just put one sentence in. How does the landing page test going? And I set this thing back and I went, christ, that is my. Fee for a month doing that, to actually produce that in that level of detail. Would have taken me a day at least, and I just rattled it off in maybe an hour because I wanted to really over ag it.
Them: So let me go through that. So there is a landing page test, which I assume means that the client created a secondary landing page.
Me: Correct.
Them: And I don't know, maybe you have a campaign. 50% traffic going to one page, 50 or the other.
Me: It's an experiment. It's an experiment on Google Ads. Experiment.
Them: And he asked you, well, how is the experiment going? Fine. And you go and tell Claude the client is asking me this.
Me: Yeah.
Them: Based on the context information and.
Me: No, I didn't do that. No, I didn't do that. I said email sync. It ran the email sync. It's labeled the emails for clients. I said, read Helen's latest email and comment on it.
Them: Okay, I comment on it. And then you get the response what it does. What?
Me: Well, it produced a report or only page report? I had to do the screenshots of the so desktop and mobile for both of them. I said, drop this in there.
Them: It was a critique on the landing page or it was just data.
Me: Is it? No, it's a test. So I. I sorry, it was. I didn't explain that very well. It was an experiment in. In Google Ads for an ad variation. They had variation was landing on different pages. So it was a. It was a landing page test as such. But the data was in. In Google sending it half and half.
Them: Yeah.
Me: So that.
Them: So it got the data from the variant test and it just produced a report on that data. So you come and look. I don't know. I mean. What? What? I was just wondering. I mean, that is so. If it's landing page, it's more about conversion rates.
Me: Yep.
Them: It's more about cost per conversion and things like that.
Me: Yep.
Them: But you talk about screenshots, so what was that?
Me: But the screenshots were the actual landing pages themselves. Where it was sending it to, so did desktop and a mobile version. And I asked it to critique the landing pages as well.
Them: The landing page critique is it was the real valuable thing from.
Me: It was. But we'd done another test earlier, another month. It was about that big of a review on that one, because I'd done it myself, and it was. It was quite favorable, this one. There was no conversions at all in the period for either of the variations. They're usually quite low anyway, and he told me why.
Them: Okay?
Me: It actually explained why.
Them: So you have. Sorry, keep interrupting. So you got your. I don't know, maybe you have a skill that goes through landing page critique. Now. Okay. Just Claude criticized landing page.
Me: Yeah. Yeah. Yeah.
Them: Okay?
Me: And as time goes on, what I might do is build some more stuff into my knowledge base. So the knowledge base now is being built upon going and looking on the web. It's built upon playbooks I've created for clients. It's built upon pro post mortems of them. Provides. I've just done one for Black Friday for a client. You know, we did this, and this happens. And my own knowledge. There's actually a section in the knowledge base which I've not run yet, which is going to be an interview phase where it's going to ask me things that I do, things that I think are good, things that I think about.
Them: Yeah, yeah.
Me: And I said to it, that's fine, but I don't want this to be my opinion. I want this to be statistics based, say. Right. Okay, well, I'll bear that in mind. So I might be saying I think we should be doing this, and it's actually wrong. Statistically, it's wrong. And I want to be pulled up on that. I don't want it to be my opinion. I want to be able to give it the input. And it's called the Rock Systems Methodology. So I want to give it that input, but I don't want that to be the. The total driving thing, because if it's wrong from the start, it's going to be wrong for everybody then. So that's why the knowledge base for me is the most important thing that is my brain.
Them: Yeah, yeah.
Me: The rest is access to to to Google Woocommerce. Got a woocommerce mcp server. I've got a shopify mcp server. That was relatively straight. It's a bit more complicated than the WooCommerce one because you got to create an app within Shopify. But now I can interrogate Shopify directly. Google Trends is a real shit. Don't bother with MCP for just awful keeps timing out, it just doesn't. Like it doesn't. It doesn't like too many API calls in one going. Google Trends does tend to use a lot. I won't. I won't bother with that analytics.
Them: So shopify mcp and I. I don't have any shopify integration. I'm not going down the mcp road. What I do is I. I have an API libraries that the way that they. That the road Cloud took, which is fine with me. And. And one talks about mcp servers. And I feel like I'm missing out on it, but it's just, you know.
Me: I don't know. Seriously, I don't know.
Them: Yeah.
Me: Sometimes you say, go and interrogate it and it'll go. I'll use the mcp. Oh, that's no word. I use an API direct API call.
Them: Okay, sorry.
Me: So I suppose I'm giving it an option. I just thought mcp servers. The right way to do it. Going back to go marble because they use MCP servers.
Them: Yeah. That's why I I By the way, I I remember Marvel, there's so much going on and too many ten pounds here. I mean, in terms of AI anyway, so this Shopify could be very interesting as well. I think. Yeah. Because, I mean, in terms of, obviously, sales. Product performance, product stock. And. And things like. Yeah, I mean, margins as well. And. What? I wonder if that's something I use. I have. I have my. My Shopify. App, which I use, but it's not linked to clothes, it's linked to my scripts. And I keep. I have a number of reports taking data which I daily but that's not been integrated into Claude onto the grain. Like it could well be, anyway. Yeah, I've been working on something like that. So, as I was saying.
Me: I know you can do this yourself, but I can send you the process for Shopify. I just drop it down and email it here? Want to pull that straight into Claude and say, I want to do it for that client.
Them: Yeah.
Me: Because it works.
Them: Yeah. How do you. How do you use the Shopify data? What do you get permission to provide? Is there a stock, for example, gives me the best sellers or. Or what products I should. I don't know in terms of a stock, what products I should stop advertising because of lowest stock or what.
Me: I've not scratched the surface. The only thing I've used it for, to start off with is I wanted to find out an overall roas for the clients.
Them: Is.
Me: Because they don't do much marketing elsewhere. So I tend to quote the Shopify figure. As the revenue and Google Ads is the cost.
Them: Yeah.
Me: So I don't know. The main thing for it. You got to jump through a few hoops. On Shopify to set up the API bit, and that was the pissy bit.
Them: I've got that already, so that's. But, yeah, I mean, that. That's. That. That's exactly how I use it. So I get the client asking me, overall, I need the rows of six.
Me: Okay? Yeah.
Them: Upon. I have this in my dashboard, which sits outside cloud, anyway. It's monitoring that daily and that's. That's how it works. But it would be cool to have. But anyway, it's not integrated because I. I still want Anyway, it is not part of my. But in a way, in terms of what else I've been building, I mean, one thing I so there is that. There's this. I was. I was saying about the light review, which saved me a few hours, and actually, it found a couple of things I would have missed. But you're right. I didn't see that. I didn't. I will do probably will do that. Those, those audit reviews I like the most that will fit them into the quote and see how we improve. I mean, that's probably going to be what is the light review and more the high level, not high level, actually. The detailed review, the deep, the real. That's probably what I can do to fit, because I still want a different audit review levels.
Me: Yeah. Yeah, yeah. And that's your. That's your value that you're putting into it. You know, to. Then you're going to get the reviews out in the style that you want them, and that is you. That's what you know, that's that. 's the bit you add to all that.
Them: Yeah, indeed. Indeed. Yes, yes. And the formatting as well. So half a half scale and that. So basically, I have these calls and sometimes I don't necessarily prepare many of the calls because I speak into my clients and I've not done four years, so I really know everybody. But for some, for some others, you need to prepare those calls. So I have a skill that does that. So I just, you know, prepare. Prepare my agenda or my meeting prep, My meeting prep document. I think that that is an issue that was initially based on one of Mike's skills, but back on my call with clientex tomorrow morning,
Me: Yeah. Yes.
Them: And he just asked that. And he gets everything into a slide, a Google Slide with the right formatting, the kind of log, everything. So preparing something like this. Okay, I'll use it twice, so we'll see.
Me: I look at you, I love it. You can't stop smiling about this as well. It's brilliant. Because that's exactly how I feel. Because you, inside your head, you go, wow, that's amazing.
Them: Yeah. Because. I probably wouldn't have done that, but if I had to do that, he would have taken me two, three hours now.
Me: Yeah.
Them: He took me to the hours to get the whole thing done. But the following call, it took me 10 minutes. And it took me 10 minutes. So I prompted waited three minutes. Get these light show already. The formatting, the words, the titles, the log, all the dates, all sorted. It took me 10 minutes to refine because it's never. I mean, it would never be Find some of redundant stuff.
Me: Correct.
Them: But it was really good because obviously went through all my slack. It's like channel communications work through my emails, my nutri notes. So it came up with a couple of things. Oh, I had totally forgotten about this. Oh, that's my point. And to be honest, there's not so much AI in that.
Me: Awesome.
Them: The AI is summarizing all the communications and so on them into a cache and then getting everything into this slideshow or the document, the Google Slide. It wasn't AI, really. It was just the app.
Me: Yeah.
Them: It was just taking the formatting, so it was not. Claude. Create a Google sheet from scratch with the client. Logan. And no, this is the template. This is the cache with all the data. It's already summarized.
Me: Yeah.
Them: Now. Am I lying? No, I think I had much to do with that. And some of the things I built is reminder. So I'm not using agents yet, but I have jobs that run all the time. Or every couple of hours. So there's one job that checks my slack communications, my emails and meeting notes every couple of hours.
Me: Yep.
Them: Ten me as lack notifications for any tasks or reminders. So there is this email from this client. These are the three reminders. And it adds that into my dashboard, which is a task management tool I just built as well as you did. It just has actually four reminders and it goes hard to approve them or not approve them, accept them, or they delete them. And that's automatically just fits.
Me: Yep.
Them: So it's really useful for notes, for meeting notes, because Granola. So I have a call. Hang up, forget about it. And with the next hour, I will get reminded. These are the actions that go from Granola to growth into slack and from slack.
Me: Yeah.
Them: Well. And then into the dashboard. Into my dashboard. And, yeah, I've got that. And I cannot forget, really, and I kind of. Kind of focus on the next goal. And then after, you know, just go. Okay, These are my notes, are the actions. Fine. This is an actual task. This is just remembering. Oh, this is rubbish. I delete that.
Me: I like the reminders thing. I think that's to. To add that on because there's a difference between tasks and reminders, isn't.
Them: Yeah, let me show you. Because we keep showing me all the time.
Me: There.
Them: I want to. I want to show up. I want to show off a bit, if I can. Let me see this response because I haven't serviced down, okay? Let me get rid of the Ultra thing.
Me: I think this is one of the things that I'm finding is I wouldn't. I couldn't sell this. At the moment, it's far too flaky to sell, you know. I mean, the number of errors it makes is quite extraordinary, especially on data. You've got to really watch it, you know, because. Oh, I didn't know you meant that. I'd just be working this for two fucking hours. What do you think I meant? I actually scroll down here as well, and it swears back at you when you. When you say to you really fucked up, that, yes, I really fucked up there.
Them: Yeah, well, yeah.
Me: Well. I ran. I ran one of Mike's skills and that said bollocks in it. I think. You know, that's Mike. That is. That really is. A nice one is slash client. Where you. If you're. If you move between clients, you kick up a new terminal and just do slash clients and then the name of the client and it loads the client up for you, so there's no ambiguity about what you're working on.
Them: Oh, yeah, I see. Yeah. Let me show you just to show up a bit. I know as impressive yours. But these dashboards and this Diabo just goes through all. But then I can select all the clients. These are Clients are really so I have. I don't know. So Shad. That's why I have reminders and tasks.
Me: Brilliant.
Them: So this task is in sync with my Google Sheet task, which I share with the client.
Me: Okay? Yeah.
Them: Because the client is checks in I don't know. So 8 inch they make I sync that with the Google sheet and the Google actually that can open and change and this this section here, this graph hub is thinking the starts with what I call in the.
Me: Yeah.
Them: In the Google sheet and these are reminders. And this is what is being fed from meeting notes from an emails. So I get, so I don't know, I got an email. I don't know if I have any. That need to approve. I may not have any to approve, but it basically will tell me. Look, this is a reminder, so I need to perform this client.
Me: Yep.
Them: I need to repair the plan for February March testing period. These are some nodes taken from my call yesterday. Some of them are duplicated. Maybe, but anyway gives me an idea and have the tasks. Fit as well, and I can go and obviously make timeline. And. And. And they have even had templates. Okay. I need to prepare a reminder kind of a task. For promos. So give me. So just give me all the steps. I just add the name, the date. Fine. Create workflow.
Me: Oh, I love that.
Them: I don't know. Window sale, for example. 20, 25, I guess. I don't know. With the sale. Gentle sales. So say, okay, fine. This is going to launch on, I don't know, it's going to be on the time unboxing day. Fine. So clear the workflow, and then based on that, I have this. Check the dates. Okay, fine. This is actually going to be, by the way, give me approximate dates and then. Label, and then I kind of blow for high DP because some of these steps will develop for some Granola. Anyway, it's just me having fun. Do I need this now? Make my life easier?
Me: Brilliant.
Them: Yes. Was it fun?
Me: Yeah. Yeah, I feel that matters, isn't it?
Them: A lot, you know? Daily briefs so I can send okay I missed nearly forgiven because my PC was switched off so I sent daily brief and it would tell me the meeting the clay might things have a day priorities reminders available for the day and for the week or prioritizing a really nice way as a slack message because I'M trying to get everything into slack.
Me: Yeah. I think, yeah, it's having that single point of communication beyond email, because I've got WhatsApp and I've got teams.
Them: Yeah.
Me: The only way I can do that is literally to select all and paste it.
Them: Yeah.
Me: That's the only way I can get it in. And it is so annoying. If the client doesn't use slack, I don't know how I can force them to do it.
Them: Yeah. Had a client who. Anyway, yes, you're right. I have also some dashboards. Have a health dashboard.
Me: Okay?
Them: Which, okay. Well, sorry, I don't know. It's not working now. How to use it for a few days. This is basically telling the state of the caches, the email cache and so on.
Me: Right. Yeah.
Them: And then I'm working on. Okay. I haven't used it for the. I was working on engaged engagement score. So the idea is, look, there's some clients who are. You know, I just forget about them because.
Me: You're right. Yeah. You're right. Yeah. It's a great one.
Them: This is kind of a score, a dashboard that will tell me, look, this client, I don't know, this is gold, silver, bronze. I have to reach 60 points every week and 60 points if I have a call. That's 30 points every email. I said every Slack. Let's check. SM is 5 points if I unless there could be some. It counts the number of changes in the Google Ads. So if I make every. Every change in Google Ads I make is 3 points, and it just scores every week and I reach it and it's. It's kind of gamifying just to make.
Me: You've done nothing. On it. Yeah. Yeah, that's very good. And do you. Do you feed into that how much they're paying?
Them: Sure.
Me: As a proportion of how much money you're right.
Them: Yes, yes.
Me: To keep it, isn't it?
Them: I think. Well, yes and no. That was one of the inputs. But I feel uncomfortable about that because I don't know. How things will evolve. So I just say it's high, low, medium priority, but essentially the same but. Yeah, and there's some but in terms of demand as well. So this is a very demanding client. So the 60 point goal level for some. For some is 60. For some it's 80 or 90, depending on how much they pay, how demanding they are. Because some guy is, you know, they're just happy to get a monthly update, and that's about it.
Me: Yeah, yeah.
Them: The weekly call. Some others will have checking badges weekly. So I'm still building it, but the idea is, look, I just go in and say, okay, every. You know, these are in good shape. I didn't speak into them. I think hundred calls with them, communicating with them, doing, doing work on Google Ads at this point is just number of changes. I don't know. It could be hitting weekly budgets and so on. And it tells me, look, these are in the red zone because you haven't spoken to them in all week. You get it?
Me: Yeah. It's. It's almost like you're saying if you went on the phone call with a client now, how embarrassed would you be? You know?
Them: Well, only get there, probably, you know, find my way around it.
Me: Yeah. Yeah.
Them: I suppose so. I. I would say no, but that's probably going to be a lot of some of that. But, yeah, there is some of that sometimes. But. But yeah, that's about it. It's kind of making it fun. So it's more finding, finding the incentive to go into that account. No one cares about, not even themselves. Because I thought some of the accounts I enjoy the most is those clients are really active. You know, they email me. They're not demanding, but they are people and generally interested to making things work.
Me: Yeah. Yeah.
Them: For them and for me and for the business. So, okay. Can we do this? I'm trying this and that, but some others, you ask them something. Oh, yeah, fine. And then nothing. For. For days, for weeks, you can be reminding them nothing. So those. I tend to neglect them. You know, they. They pay. They don't complain. Well, don't complain that you go to a call and they. Anyway, it doesn't matter. So, yeah, it's kind of making it fun to me to find other reason to go into that and work for them, because otherwise. Just forget about them.
Me: Y. Eah. Yes. Yeah. You do? Yeah. No, I think that's brilliant. I. I have a. I have a client. It's slightly off topic, but they do a kids toy. I think I've spoken to you about them before. And I, he. He's been. We've been. I've been working out strategy to increase budgets and change target roas and so on. And over Christmas, it just goes nuts. And they always run out of stock because it just gets out of hand. I know. I looked at it the other day and you know when you just look at numbers and you don't really go, Yeah, I'm not looking at that as actual pounds. I'm just looking at that as a number. And I've got to increase, decrease, whatever. And I looked at it the other day. Because I wanted one of these toys for my nieces. Son. So I emailed him and I said, it is the only chance, you know, you. You could do me a deal on one of these. And I looked at what his Q4 sales were in the US since October. It was $9 million. And I looked at how much I charge him. And what and when. If he doesn't give me this for nothing, I'm going to go absolutely nuts. Thankfully, he emailed back very, very quick. Oh, yes, you can have whatever color you like. You know, I get it straight away, blah, blah. And I'm looking and going, yeah, you will, won't you? But it was funny how it's like that engagement thing. For the rest of the year, I won't hear from him. And then the Q4. That's when it's all going to go absolutely nuts. But all that preparation for. For the rest of the year has produced those figures now. So it's one of the best success stories, that. But actually doing budget changes because one minute he'll say, I we're running out of stock. Slow it down. Next minute I say, we found some stocks, so can you increase it? And I'm just going in and just saying, saying, read the email. Come up with an email back to him. It's about an A4 page long. This email. Send it off to him. The action, the changes and documents it. So send another email, say, I've just done this. And that's one of the nicest because I, I, it's funny looking at your, your dashboard, I look at it go, that looks really polished. That, that's a really nice way to do it. I've been more textual based than anything else. I'm working in within the system, within Cursor rather than building metas. Manager is outside Cursor. I put it onto a browser, but everything else has been text based. And I'm just running it straight from text. Eventually I'm going to have enough stuff in there to be able to go, okay. Let's gather all this information together. And do a planning session one day to say, let's try and create a dashboard that grabs all this stuff together, and it makes sure I have a universal approach. It's only been recently I've said I've realized that the skills I'm creating weren't universal skills. I've been working on a client and saying I want to do this. And they say, right, well, I've done that. Then go to another client and say, right, can you do this? Why? I don't have that skill. And you go, oh, Christ, no. It's not actually universal skill I've created. So. Okay. We'll go and look in. Go and look in such and such. About this. The skill in there or it'll go and find it. He said there's a skill in such and such a client. Do you want me to use that one? Well, yeah, I do, but I also want it to be universal skill. And it was that structuring of the directory. That you look at you looking at that on a regular basis and going, hang on, he's not writing. And like doing tidy ups. All like the tasks I don't use. I use Google Tasks very infrequently now. Mainly it's just the system task list that I use, but it was saving them in different places. It wasn't saving the task. JSON in the same place all the time. So I got it to tidy all that up and then it the next time you go see, I can't find the tasks. And another skill. Was referring somewhere else for the task. So it's that. It's making sure everything works together. It's been quite complicated. And all it took was the right prompt. And you go, yeah, yeah, I can do that. Yeah, yeah, no problem. Why don't you just ask me? You know? Yeah. And you think, oh, God. So then going back through it. So I think that's why I like terminal, is to go back and go, well, why is that there? That shouldn't be there. And then it starts to unearth other things, doesn't it? So I think eventually, once Christmas is over and I've got some time, I think I would like to do some sort of dashboard and then I can say, well, I don't have to go and do client, blah, blah, blah, it will just go and do that in the background.
Them: Yeah. Let me, because I spend days fighting for this. The reason I moved from having a web UI to going back into cloth was because I cannot use scales. From the web ui, so those skills are not available to the API. There is a cloud. I ask a question to Mike, which is in the, in the. In the app, in the 1820 app. Passing up on actually got really confused with my questions, I think. But the point is that I struggle with that because I was very keen on using a web ui, as I showed you the other day.
Me: Oh, really? Yeah. Yeah.
Them: How to abandon that, give up on that. And go back into the. Not the terminal, but kind of the black screen. Because I could not use the skills. And it's fine. I mean, it's no big deal. Actually, I find it fine. But that was big deal for me.
Me: Then, wouldn't you? Rather than use the skills you'd have to build a proper app. Because you could use them. You could use like light railway or. Or, you know, a lot of it is flask cap, isn't it?
Them: I don't know. I mean. There was no. Okay, I'm maybe not inside your question. There was no way available. That I could find. I asked. I mean, I went through everything and I asked. God, I asked. Anyway, there was no way available it will be to invoke, kind of invoke the skills I had in my app.
Me: Right. Oh, I see.
Them: Through the API, because the API connects directly to, I guess, the cloud API. And that that didn't make the skill available because it's sitting in my app.
Me: Okay? And this is funny because we get to this sort of. This sort of stage, it is beyond my knowledge. Sometimes in the way it works. It's like the Railway app. You're using that very simple example of the. Of taking the picture of the. The. The recipe cards. I know I can't do that on my own website, so. Got me, like, you've got the ad success one. I can't create a subdomain on there and just run it on there because it needs. It needs something. It needs Python anywhere is it. It's a. It's. It's. It's the thing that you would put on your own app so you can run Python on your. On your.
Them: Some driver. I'm going to buy that anyway.
Me: But it facilitates being able to run Python scripts on there. But then you get into the problem of, yes, the cloud interface. You're going to have to use cloud API, then. Which then starts to invoke cost, which I've done on some of my. Unbeknownst to me, I've. I've been incurring abi costs on there.
Them: When we use cloud code, we use API costs, so. So I have. Well. I have Cloud Max, and that's for Cloud AI. AI. And that. That is outside the app. That. That's. That's me playing up with some other things.
Me: Yes. Y.
Them: And then we have code, and that's linked to the Control API. And those. Yeah, you have to keep putting money into that.
Me: Ep. But if you've got Claude. If you've got Claude, Max.
Them: Yes.
Me: And you're running Claude through your cursor.
Them: Yeah.
Me: You're not using any API. There's no additional API costs on that. That's all encompassed within your Claude Max.
Them: Okay, I'm missing that.
Me: Yeah.
Them: That's not.
Me: You have an allowance in your Claude. Max.
Them: Sorry. Let me. Let me share my screen. So I have. So. There is. This is claude. Okay? And I have max plan. Okay? And the campaign, whatever. And then this is one, and the other one I've got is entropic. And let us see. Because I was getting. Yeah. So, yeah, I have entropic API, and this is. This is what I'm using and extending. So I have spent two hours in the last week, so I've not really. But the point is, I'm buying credits.
Me: Yep.
Them: I mean.
Me: Yeah, I. I do as well. There's only certain things within your brain. That actually uses those credits, and it is the ones that are running independently.
Them: Okay? I don't know.
Me: If you're running like a, a launch agent or something like that, that's running without cursor, without you interacting via cursor, it will use those, those API calls. And this is why you need to look at your launch agent and make sure you're using HeyQ, the cheap one. When you use a lot of Claude.
Them: Yeah. Yeah.
Me: If you're using the Opus 4, Opus 4.5, it eats those quite quickly. But ask the question. Of claude. When do I use? When am I incorrect incurring API costs considering I already have a claw max and it will reveal quite a lot of things to you because I had this conversation with it. The other day. And it. It revealed a lot because it'll say, well, this is where you're incurring those costs. These are the agents they're incurring. Do you need to use this level of Claude, Claud? The Claude model to do this? And some instances you can pull it back even further. But $2 is neither in or there is it.
Them: Yeah.
Me: That's why it's not going up quickly, because your Claude Max account has been used within. Within your cursor.
Them: Spending. I don't know how we know how. How does it do it? Because I have added my entropic API. My entropy key. API key. Sorry. The topic API keys. I haven't given it any clue. AI key. So how would it know that?
Me: Wasn't there a no author similar to an oauth right at the very beginning?
Them: Yeah, but I thought. Okay, okay, it's easy. Sometime now. So I have. And I'm still showing that we have this file code. This is the one I gave it. Key for testing. I'm not using that. But there is nothing. Include AI, which is the one I'm showing you now. There's nothing.
Me: I don't know. I. I genuinely don't know how it connects, but it knows you've got a. A Claude Max account.
Them: Okay, fine.
Me: We must have done it at some time when we set the whole thing up. Like whether it. Whether. Whether it's in. Because it's probably in. In cursor, isn't it? Within cursor. You're telling it you've got an account?
Them: To be frank. Why not to be found? I'm trying all the time. I'm finding very frustrating. The conversations I'm having with. I mean, well, that's not true because my lack of vision was useful. But anyway, I find a call is not always really clear about. APIs and keys while using this of that. But not. Not. But I'm not being. I don't. I remember not because my Dasco. I mean, there was a time. There was one day when it got. Because I. I remember when it had my last. My late. My last call with you. I felt a bit frustrated. About how things were going. I was getting all these talking issues and so on. And.
Me: This terminology. A lot of it, isn't it? A lot of it is terminology because it's new terminology to us.
Them: Yeah, but there was. There was something, anyway. I. I got past that point. I think I. I was able to trust I understood thing about tokens, I got more relaxed and because I understood the context stock in his 200,000 as opposed to 12,000.
Me: Yeah. It's so annoying when it compacts as well. That's really, really frustrating.
Them: He was really confused the way and I was getting some Airbnb anyway. You know, I just got past that point. And I obviously understood. I kind of used the skills. Within the web ui. So I moved away from the UI and I kind of simplified things. I made more confident and anyway,
Me: Y. It's a proper tool, though, isn't it? It is a proper tool. It helps us with our job. I say, you couldn't necessarily give this to someone, say, go and use that, then you can go and do it. It's not like that at all, and that's what I love about it. That it is. You know, you're downloading from your head. Stuff like. Like the landing page. It just go go look back through my emails. I can't remember when the landing page test started. Anyway went and found it. And you just go, God, I never remember that. You know, and it's just joining the dots with all that. And, like, creating monthly reports. What have I done during the month for this client? I have no idea. What were the results of what I've done? Well, there you go. It's. It just. It just does. It. It's that completeness that. It's really quite scary, but I'm. I'm. I'm absolutely. As much as your grin tells me, I'm really enjoying it as much as you are.
Them: So really to me when we are in a situation now do you have a hard stop now or you can find so I'm not going to take all the time.
Me: Yeah. No, no, no.
Them: I want to go and take a nap. I don't recall this morning. I did a presentation, so I'm really tired, but anyway.
Me: I just cancel my call at 2:00 and I can't be doing with this.
Them: No, no, no. I was looking forward to it.
Me: No, no. I just canceled my call at 2:00. Yeah, I didn't know. I did it early on this morning. I just. I didn't have the capacity today. I've had to take my sister to the hospital this morning for an appointment, and it's just. It's been full on all day. The last thing I wanted to do was speak to a client. This has been a good relief, I think.
Them: Okay, Fine. Sorry. Finally. Go well, we'll catch up another time. And. And go into some of the things as well.
Me: Yeah, absolutely. Yeah, I'm. I'm happy to do this every week. It's the voyage of discovery, and no one else understands what the hell I'm talking about.
Them: Let's do something. Okay, fine. If you you're happy to do wakeling, can we. I mean, does is this time work for you? Quickly?
Me: Yeah. Yeah. Yeah. Yeah.
Them: Yeah. So wonderful.
Me: It's. There will be some Fridays I can't do. Sometimes we go away for the weekend. But it's not. There's. There's nothing in the near future. We can always move it around, can't we? Let's just put a line in there. And then we can move if we need to.
Them: We done? We can skip from time to time. We're going to get bored of each other, so. Yeah, we can. Yeah, that's fine. Okay, I'll make it. I'll make it regular. Well, not every week, anyway. Yeah, with a few exceptions. I will make it regular. So, you know, we can always escape if it doesn't work or we have lots of things.
Me: Well, it's. It's good. It's good to talk about this because, you know, all of you just come up with ideas, don't you? And you only really realize them. I've recorded it again. Like, I've stuck this on Granola. I literally do it for everything now. And even that, it's amazing what it pops up with.
Them: Pretty addictive. Anyway, but just go. And again, I've heard there's somebody from, from a previous call with a client and I, I just got. And the summary starts for good. And again, we're always scratching the surface because this templates, these recipes and all these things with Granola make. When I say circulars, we're probably getting 70% of the value anyway. But this. There's more that. Anyway, I mean, just that. Just the basics is. Is plenty.
Me: And that's all I use, because I'm just using the raw data. I'm just using Granola as a way to gather the data, put it into the Google Doc, which you told me about, using Zapier. And then put it into. Into the system. Fantastic. That's a great way to do it.
Them: Did you send? Do you give cloth? All the trans. All veterans. All the transcript or the notes from Granola?
Me: Yeah, all of it.
Them: Because, I mean, I only did it. I'm always thinking of tokens, which just. I think I. I got traumatized with tokens that first week, and I can stop myself. But. But the summaries are really so good. But yeah, I mean, transcripts. I mean, you have calls that can take go like this one, right? By the way, that's fine. I got footnotes. But I can always provide the transcripts if needed.
Me: Yeah.
Them: But I'm just thinking if I'm missing out something. But I find the note so good that I don't really. I don't know, I may be going. The transcripts may be good for kind of exploratory calls with new clients, but the regular calls. Sorry, I'm just thinking. Out loud.
Me: No, no, it's fine. No, you're right, because there may be some nuance in there that you're missing, or there may be some detail that the summary is not actually capturing. And you could always go back on there and ask, you know, did the client ever mention this? Well, that might not be in the summary.
Them: I found myself going to Granola about a couple of things. So I wasn't sure about the dates of a promo. I went into Granola and asked, what were the dates of the promo? And Granola is great. I mean, they may be using gold code in the back end. And it gave me the perfect answers. Now I could have get the trusted in through clothes and then ask the question to close and probably that would be better because then I have all the information I need there.
Me: And I don't want to go anywhere. I don't want to go to multiple places. I think that's the thing. I don't want to be going to all these different places to get data. I just want to go to Claude and say, go and get me the data, wherever it is. Did we ever talk about this with such and such a client? Well, it could have been a teams meeting. It could have been a Granola import. It could be in an email. I don't want to have to go to three different places. Just want to go to one and say, give me all the details about this. It's ever been discussed. And it's just so annoying with teams just having to cut and paste. Bang. But remembering to do that, I'm setting a task to do it. You know, so that every. I've got recurring tasks every seven days or something. It'll pop up. And I say, all right, I need to do that. And then because the task. If I say completed, carry out this task. Save. Put that into process. My notes. I put that into Claude and it goes and reads. So what's happening in task is when you. When you take my notes. It copies that into downloads folder. Then I go to Claudia. If I say process my notes, it will read that download folder. And then go and do whatever I've asked it to do within the. Within the task. But everything's visible in the task. I think that's the nice flow of all that, that you don't need to remember the detail, that you've already saved it within the task. And you don't need to know what to say to Claude, because it's already in attack what you. What you want to achieve from it. So it's. Yeah, it's just a. It's just a nice kind of flow to it all. And certainly it's all done within. Within Claude as well. It's proper techie, though, isn't it? I feel a proper geek. Really do feel like a geek. It's great.
Them: I'm thinking, what next? I'm thinking, okay, this is Google Ads, but what next?
Me: Yeah.
Them: I'm thinking about other projects because, as I said, everything is possible now. So all the things I thought of doing that it felt, well, you know, I'm not going to have two years to build this. I can build in two weeks.
Me: Yeah, yeah. Yeah. I tell you one thing to be very careful of. If you go down the Microsoft ads mcp. That is a bitch. As ever, Microsoft ads is a pain in the ass. You've got to use an Azure Cloud account to do it. I was on the phone. For pretty much two hours with Microsoft trying to sort it out. It was just a nightmare to the extent where I've set it up, the necessary links and so on. I've not even touched it since. It just sucked the lifeblood out of me. And you think, well, I don't. I don't really. I'm not up to date with Microsoft ads as much as I am with Google Ads, so maybe it'd be a good thing with code to use it to. To optimize things. I can't be asked. You know, the amount of money it generates. I cannot be bothered at all. It's the usual thing. What do I do? Do I spend an hour on Microsoft ads or an hour on Google? It's a no brainer, isn't it? You know, I'd rather spend an hour doing bloody recipe cards than being on my consultants.
Them: Here. It's getting worse. So destroying going through the amount of Microsoft ads a ui. It's just like what I'm doing Megaway.
Me: Yeah. Yeah, yeah, yeah, you're right, you're right.
Them: Anyway. Well, have a good weekend.
Me: Lovely. Yes. Enjoy that. Thank you, sue.
Them: Take care.
Me: Have a good mate. Bye bye now.
