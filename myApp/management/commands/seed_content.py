from django.core.management.base import BaseCommand
from myApp.models import (
    Page, Section,
    HeroSection,
    StatItem, StatisticsSection,
    CredibilityItem, HighlightStat, CredibilitySection,
    Testimonial, TestimonialsSection,
    PainPoint, PainPointsSolutionsSection,
    DifferentiatorCard, WhatMakesMeDifferentSection,
    Publication, FeaturedPublicationsSection,
    Service, ServicesSection,
    MeetKimHerrleinSection,
    MissionSection,
    FreeResourceSection,
    SocialLink, FooterLink, FooterSection,
)


class Command(BaseCommand):
    help = 'Seed the database with initial content from the brand brief'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with initial content...')
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        HeroSection.objects.all().delete()
        StatisticsSection.objects.all().delete()
        CredibilitySection.objects.all().delete()
        TestimonialsSection.objects.all().delete()
        PainPointsSolutionsSection.objects.all().delete()
        WhatMakesMeDifferentSection.objects.all().delete()
        FeaturedPublicationsSection.objects.all().delete()
        ServicesSection.objects.all().delete()
        MeetKimHerrleinSection.objects.all().delete()
        MissionSection.objects.all().delete()
        FreeResourceSection.objects.all().delete()
        FooterSection.objects.all().delete()
        
        # ==================== HERO SECTION ====================
        self.stdout.write('Creating Hero Section...')
        hero = HeroSection.objects.create(
            headline="You've Built Success. Now Build a Life That Feels Like Yours.",
            subheadline="You've led teams, built a career, maybe raised a family. But somewhere in your 40s or 50s, you realized you're living on someone else's terms — fragmented, performing, moving through days that don't feel like yours.",
            body_text="What you're sensing isn't a crisis to fix. It's a calling to redesign.\nReinvention is your birthright — an invitation to come home to yourself with clarity, creativity, and courage.",
            quote_text="Reinvention is your birthright. It's not a crisis, it's a calling.",
            quote_attribution="Kim Herrlein",
            primary_button_label="Schedule Your Free Clarity Call",
            primary_button_url="#clarity-call",
            primary_button_variant="primary",
            secondary_button_label="Explore the Golden Thread Spiral™",
            secondary_button_url="#golden-thread",
            secondary_button_variant="link",
            icon="fa-solid fa-compass",
            image_url="https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=800&h=1000&fit=crop&q=80",
            image_alt_text="Kim Herrlein, transformational coach, smiling in a softly lit space",
            layout_variant="text_left_image_right",
            background_style="dark_band",
            show_section=True,
            emphasize_as_key_section=True,
            order=1
        )
        
        # ==================== STATISTICS SECTION ====================
        self.stdout.write('Creating Statistics Section...')
        stats = StatisticsSection.objects.create(
            headline="Your Desire for Reinvention Is a Powerful, Collective Trend.",
            intro_text="The drive you feel to reclaim your life is part of a global movement. You are not alone in this intentional reinvention.",
            primary_button_label="Explore How I Can Guide You",
            primary_button_url="#programs",
            primary_button_variant="primary",
            layout_variant="cards_grid",
            background_style="dark_band",
            show_section=True,
            order=2
        )
        
        StatItem.objects.create(
            section=stats,
            label="1 in 3 professionals aged 45–54",
            value="1 in 3",
            description="are planning a significant career change — this is the decade for intentional reinvention.",
            icon="fa-solid fa-chart-line",
            order=0
        )
        StatItem.objects.create(
            section=stats,
            label="73% of women seeking a career shift",
            value="73%",
            description="are doing it for greater fulfillment, not just financial gain.",
            icon="fa-solid fa-people-group",
            order=1
        )
        StatItem.objects.create(
            section=stats,
            label="Research shows",
            value="",
            description="that this kind of transition deepens self-awareness, resilience, and empowerment — the same muscles strengthened in Insight Seeker's frameworks.",
            icon="fa-solid fa-brain",
            order=2
        )
        
        # ==================== CREDIBILITY SECTION ====================
        self.stdout.write('Creating Credibility Section...')
        credibility = CredibilitySection.objects.create(
            headline="Decades of Experience. A Life of Lived Truth.",
            subheadline="What qualifies me to guide women through reinvention.",
            intro_text="I don't teach what I haven't walked. I've spiraled through loss, collapse, and deliberate reinvention — emerging with tools that work in real life.",
            image_url="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&h=800&fit=crop&q=80",
            image_alt_text="Kim Herrlein speaking on stage at a hospitality summit",
            primary_button_label="Explore How I Can Guide You",
            primary_button_url="#programs",
            primary_button_variant="primary",
            layout_variant="two_column_text_image",
            background_style="light_surface",
            show_section=True,
            order=3
        )
        
        CredibilityItem.objects.create(
            section=credibility,
            title="Credentials",
            body_text="M.A. in Psychology · B.S. in Communications · NLP Practitioner.",
            icon="fa-solid fa-graduation-cap",
            order=0
        )
        CredibilityItem.objects.create(
            section=credibility,
            title="Author & Speaker",
            body_text="3x Amazon Best-Selling Co-Author · 12+ podcast features · STR Hospitality Summit Speaker (April 2025).",
            icon="fa-solid fa-book-open",
            order=1
        )
        CredibilityItem.objects.create(
            section=credibility,
            title="Leadership",
            body_text="Decade-long mastermind facilitator and first official licensee of Connect for Success — creating sacred spaces for transformation in coaching, events, and community.",
            icon="fa-solid fa-users-gear",
            order=2
        )
        CredibilityItem.objects.create(
            section=credibility,
            title="Entrepreneur",
            body_text="Founder of Purveyors of Leisure, designer of The Fainting Couch Boutique Hotel, and founder of Always Receptive — leading a 6-person team to multi-million revenue in hospitality.",
            icon="fa-solid fa-building",
            order=3
        )
        
        # ==================== TESTIMONIALS SECTION ====================
        self.stdout.write('Creating Testimonials Section...')
        testimonials = TestimonialsSection.objects.create(
            headline="How Women Are Spiraling Upward",
            subheadline="Women who discovered clarity they didn't know was possible.",
            primary_button_label="Begin Your Own Transformation",
            primary_button_url="#programs",
            primary_button_variant="primary",
            layout_variant="cards_grid",
            background_style="light_surface",
            show_section=True,
            order=4
        )
        
        Testimonial.objects.create(
            section=testimonials,
            quote="It's more than a class. It's a game changer. I feel more confident, more trusting of my intuition, more resilient when obstacles arise, and more inspired to bring my ideas into the world. Kim fostered a genuine sense of community — our cohort became cheerleaders for one another. If you're looking for coaching that is equal parts heart, insight, and strategy, I wholeheartedly recommend her.",
            name="Lindsey Rosen",
            image_url="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&h=200&fit=crop&q=80",
            image_alt_text="Testimonial from Lindsey Rosen about working with Kim Herrlein",
            order=0
        )
        Testimonial.objects.create(
            section=testimonials,
            quote="I discovered that insight isn't something you wait for. It's something you practice into being. These frameworks gave me enduring tools for growth. Kim guided me with such skill and care, helping me personalize everything into my daily life. By the end, I had both practical tools and a profound mindset shift.",
            name="Lisa Sunde",
            image_url="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200&h=200&fit=crop&q=80",
            image_alt_text="Testimonial from Lisa Sunde about working with Kim Herrlein",
            order=1
        )
        Testimonial.objects.create(
            section=testimonials,
            quote="From the first session, Kim created a space where curiosity and courage felt natural. Her expert guidance and carefully crafted exercises helped me peel back layers of self-doubt and reconnect with my deepest creative instincts. I gained tangible tools and a complete shift in mindset.",
            name="Suzzanne Simonian",
            image_url="https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=200&h=200&fit=crop&q=80",
            image_alt_text="Testimonial from Suzzanne Simonian about working with Kim Herrlein",
            order=2
        )
        
        # ==================== PAIN POINTS & SOLUTIONS SECTION ====================
        self.stdout.write('Creating Pain Points & Solutions Section...')
        pain_points = PainPointsSolutionsSection.objects.create(
            headline="What's Actually Holding You Back?",
            subheadline="Recognition and realization are the first steps toward realignment.",
            golden_thread_quote_text="The journey isn't linear. It's a spiral. And every round brings you closer to alignment.",
            golden_thread_quote_attribution="Kim Herrlein",
            primary_button_label="Start Your Spiral Today",
            primary_button_url="#programs",
            primary_button_variant="primary",
            layout_variant="stacked_pairs",
            background_style="dark_band",
            show_section=True,
            order=5
        )
        
        PainPoint.objects.create(
            section=pain_points,
            pain_quote="I feel emotionally fragmented. Everything's pulling in different directions.",
            description="You're juggling leadership, family, and your own ambitions. Your mind is noisy. Your heart feels distant from your purpose. Success in one area seems to cost you another.",
            what_changes_label="What Changes",
            what_changes_body="Awareness brings the pieces into view. You see the fragmentation clearly and begin designing from alignment instead of obligation.",
            icon_pain="fa-regular fa-face-frown",
            icon_solution="fa-solid fa-arrow-up-right-dots",
            order=0
        )
        PainPoint.objects.create(
            section=pain_points,
            pain_quote="I've lost myself somewhere between achievement and approval.",
            description="Years of performing have created a gap between who you are and who you present to the world. You're excellent at reading the room — but it has cost you your sense of self.",
            what_changes_label="What Changes",
            what_changes_body="Acceptance softens the resistance. You honor both your journey and your truth. Evolution isn't betrayal. It's alignment.",
            icon_pain="fa-regular fa-face-frown",
            icon_solution="fa-solid fa-sparkles",
            order=1
        )
        PainPoint.objects.create(
            section=pain_points,
            pain_quote="I want to lead from my truth, not manage an image.",
            description="Leadership feels exhausting because you're protecting a version of yourself instead of leading from your center. Boundaries blur. Energy drains.",
            what_changes_label="What Changes",
            what_changes_body="Accountability is reclaiming your agency. When you know who you are and lead from that knowing, boundaries and brilliance can coexist.",
            icon_pain="fa-regular fa-face-frown",
            icon_solution="fa-solid fa-arrow-up-right-dots",
            order=2
        )
        PainPoint.objects.create(
            section=pain_points,
            pain_quote="I know I need to change. I just don't know where to start.",
            description="You've read the books, listened to the podcasts, tried the strategies. The concepts make sense. But nothing has stuck. The heaviness remains.",
            what_changes_label="What Changes",
            what_changes_body="You don't need more information. You need presence, structure, and community — tools you can use daily, and the reminder you're not spiraling alone.",
            icon_pain="fa-regular fa-face-frown",
            icon_solution="fa-solid fa-sparkles",
            order=3
        )
        
        # ==================== WHAT MAKES ME DIFFERENT SECTION ====================
        self.stdout.write('Creating What Makes Me Different Section...')
        different = WhatMakesMeDifferentSection.objects.create(
            headline="Transformation by Design",
            subheadline="How my approach stands apart from typical coaching.",
            primary_button_label="Discover Your Alignment",
            primary_button_url="#programs",
            primary_button_variant="primary",
            layout_variant="four_column_grid",
            background_style="light_surface",
            show_section=True,
            order=6
        )
        
        DifferentiatorCard.objects.create(
            section=different,
            title="The Art of Alignment",
            body_text="You make decisions from your core values, not from obligation or approval.",
            example_text="you stop saying yes to every meeting and start protecting your creative time. Your boundaries and brilliance coexist.",
            order=0
        )
        DifferentiatorCard.objects.create(
            section=different,
            title="The Science of Creativity",
            body_text="Rooted in Stanford's 'Creativity in Business' curriculum and NLP, we reframe your story and rewire your nervous system.",
            example_text="'I'm stuck' becomes 'I'm spiraling upward with tools.'",
            order=1
        )
        DifferentiatorCard.objects.create(
            section=different,
            title="The Soul of Connection",
            body_text="You don't spiral alone. In intimate groups, real struggles — people-pleasing, guilt, over-functioning — are met with shared language and support.",
            example_text="Collective witness transforms what isolation cannot.",
            order=2
        )
        DifferentiatorCard.objects.create(
            section=different,
            title="The Golden Thread Spiral™",
            body_text="A non-linear framework guiding you through Awareness, Acceptance, Accountability, Action, and Acknowledgement — again and again, at deeper levels.",
            example_text="You ascend, you don't 'finish.'",
            order=3
        )
        
        # ==================== FEATURED PUBLICATIONS SECTION ====================
        self.stdout.write('Creating Featured Publications Section...')
        publications = FeaturedPublicationsSection.objects.create(
            headline="Thought Leadership Through Story",
            subheadline="Books that create permission for your own transformation.",
            layout_variant="cards_row",
            background_style="light_surface",
            show_section=True,
            order=7
        )
        
        Publication.objects.create(
            section=publications,
            title="Heal to Lead: Stories to Turn Your Wounds Into Wisdom",
            description="Twenty-four leaders share how they transformed deep trauma into purpose, removing the veil on mental health, addiction, abuse, and motherhood. Their courage shows what becomes possible when you look within and accept help.",
            button_label="Get Your Copy",
            button_url="#",
            image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300&h=400&fit=crop&q=80",
            image_alt_text="Cover of Heal to Lead: Stories to Turn Your Wounds Into Wisdom",
            order=0
        )
        Publication.objects.create(
            section=publications,
            title="Transforming Pain Into Purpose: Triumphant Tales of EmpowHERment",
            description="Courageous women open their hearts about turning their deepest wounds into purposeful lives. In life's darkest moments, they chose healing — and their stories prove that new beginnings are always possible.",
            button_label="Get Your Copy",
            button_url="#",
            image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=400&fit=crop&q=80",
            image_alt_text="Cover of Transforming Pain Into Purpose: Triumphant Tales of EmpowHERment",
            order=1
        )
        Publication.objects.create(
            section=publications,
            title="Hospitable Hosts: Inspiring & Memorable Stories from Airbnb Hosts Around the World",
            description="Professional hosts from seven countries share how they found financial freedom and built businesses that changed their lives. Their stories of memorable guests, unexpected partnerships, and personal transformation will move you.",
            button_label="Get Your Copy",
            button_url="#",
            image_url="https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=400&fit=crop&q=80",
            image_alt_text="Cover of Hospitable Hosts: Inspiring & Memorable Stories from Airbnb Hosts Around the World",
            order=2
        )
        
        # ==================== SERVICES SECTION ====================
        self.stdout.write('Creating Services Section...')
        services = ServicesSection.objects.create(
            headline="Choose Your Path to Alignment",
            subheadline="Find the right journey for where you are right now.",
            intro_quote="Women entrepreneurs will experience clarity to discern, confidence to choose, conviction to act, and a compassionate and endearing community to cheer them on.",
            intro_quote_attribution="Kim Herrlein",
            layout_variant="cards_grid",
            background_style="soft_gradient",
            show_section=True,
            emphasize_as_key_section=True,
            order=8
        )
        
        Service.objects.create(
            section=services,
            name="Clarity Catalyst Journey (CCJ)",
            short_label="8-Week Live Online Course",
            description="For women defining what they actually want and embracing transformational change. You'll uncover what's truly happening, release judgment, reclaim agency, and take aligned action toward clarity.",
            bullets=[
                "Live group sessions with experiential exercises, journaling, and breathwork.",
                "Peer accountability and practical tools you can use daily.",
            ],
            cohort_details="Max 20 women per cohort. Offered 3x per year. Vetting required.",
            primary_button_label="Apply for the Next Cohort — Your clarity is waiting.",
            primary_button_url="#ccj",
            primary_button_variant="primary",
            image_url="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&h=400&fit=crop&q=80",
            image_alt_text="Woman journaling at a table, soft natural light",
            icon="fa-solid fa-lightbulb",
            order=0
        )
        Service.objects.create(
            section=services,
            name="Creative Action Journey (CAJ)",
            short_label="8-Week Live Online Course",
            description="For women with a clear vision who are ready to move with conviction and creativity. You'll turn vision into momentum, blocks into breakthroughs, and intention into real-world results.",
            bullets=[
                "Live sessions on creative problem-solving and aligned action.",
                "Cohort accountability, weekly check-ins, and integration practices.",
            ],
            cohort_details="Max 20 per cohort. Offered 3x per year. Vetting required.",
            primary_button_label="Apply for the Next Cohort — Your vision deserves momentum.",
            primary_button_url="#caj",
            primary_button_variant="primary",
            image_url="https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop&q=80",
            image_alt_text="Woman moving, sticky notes or whiteboard creativity",
            icon="fa-solid fa-palette",
            order=1
        )
        Service.objects.create(
            section=services,
            name="Connect for Success Mastermind",
            short_label="Monthly Community for Women Entrepreneurs",
            description="An exclusive circle for women entrepreneurs and leaders. Monthly gatherings with peer feedback, collective problem-solving, and the witness of women who truly understand.",
            bullets=[
                "Monthly live sessions and peer advisory.",
                "Online community and optional seasonal retreats.",
            ],
            cohort_details="Cohorts of up to 12. Annual commitment.",
            primary_button_label="Apply for the Next Cohort — Rise alongside women in your spiral.",
            primary_button_url="#mastermind",
            primary_button_variant="primary",
            image_url="https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600&h=400&fit=crop&q=80",
            image_alt_text="Small group of women around a table",
            icon="fa-solid fa-users",
            order=2
        )
        Service.objects.create(
            section=services,
            name="1:1 Alignment Coaching",
            short_label="Personalized Transformation",
            description="For women navigating a major life or business transition who need dedicated support. Together, we move through the full Golden Thread Spiral™ to design your next chapter with clarity and courage.",
            bullets=[
                "12 weekly 90-minute sessions via Zoom.",
                "Personalized assessment, custom exercises, between-session support.",
            ],
            cohort_details="3-month minimum. Limited availability.",
            primary_button_label="Book a Consultation — Let's explore your path forward.",
            primary_button_url="#coaching",
            primary_button_variant="primary",
            image_url="https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop&q=80",
            image_alt_text="Two chairs facing, or one woman in reflective moment",
            icon="fa-solid fa-handshake",
            order=3
        )
        Service.objects.create(
            section=services,
            name="Elevate Retreats",
            short_label="1–3 Day Immersive Experiences",
            description="Step away and transform deeply. These intimate retreats bring the Golden Thread Spiral™ to life through workshops, creative exercises, breathwork, and community connection.",
            bullets=[
                "1–3 day in-person experiences.",
                "Groups of 12–20 women.",
            ],
            cohort_details="Offered seasonally.",
            primary_button_label="Stay Updated on Retreat Dates — Transform in person with women in your spiral.",
            primary_button_url="#retreats",
            primary_button_variant="primary",
            image_url="https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=600&h=400&fit=crop&q=80",
            image_alt_text="Nature setting, women walking on a path or gathered in circle",
            icon="fa-solid fa-mountain",
            order=4
        )
        
        # ==================== MEET KIM HERRLEIN SECTION ====================
        self.stdout.write('Creating Meet Kim Herrlein Section...')
        meet_kim = MeetKimHerrleinSection.objects.create(
            headline="A Story of Loss, Reinvention & Generational Healing",
            subheadline="How collapse became clarity. How survival became design.",
            body_text="""At 21, Kim lost her mother at 44 — a woman who spent her life in silence and self-abandonment. That loss sparked a vow: her mother's story would not become hers.

Years later, after a painful divorce, financial collapse, and the loss of her daughters' father to suicide, Kim stood in front of a mirror and realized: she didn't hate herself — she hated the life she had settled into. If she could see that clearly, she could choose differently.

That moment became her choice point. Using the same tools she now teaches — presence, acceptance, accountability, and aligned action — she rebuilt everything: her identity, her work, her family, her impact.

As founder of Purveyors of Leisure and CEO of The Fainting Couch Boutique Hotel, she discovered her true gift wasn't just in hospitality logistics, but in guiding communities through transformation. With a Master's in Psychology, NLP certification, and the hard-won wisdom of her own spiral, she created Insight Seeker to hold space for women to reconnect with themselves and rise into aligned leadership.""",
            quote_text="Empowering women to rise up, feel seen, and believe in their impact is my passion. Authentic alignment means women will move boldly in this world.",
            quote_attribution="Kim Herrlein",
            image_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=600&h=800&fit=crop&q=80",
            image_alt_text="Kim Herrlein, founder of Insight Seeker, standing outdoors in natural light",
            primary_button_label="Schedule Your Free Clarity Call",
            primary_button_url="#clarity-call",
            primary_button_variant="primary",
            layout_variant="two_column_text_image",
            background_style="light_surface",
            show_section=True,
            order=9
        )
        
        # ==================== MISSION SECTION ====================
        self.stdout.write('Creating Mission Section...')
        mission = MissionSection.objects.create(
            headline="What I'm Building & The Impact I'm Committed to Creating",
            body_text="""I guide high-achieving women from emotional fragmentation to empowered reinvention, so they can live in authentic alignment and emotional wholeness.

I facilitate emotional liberation by helping women break free from people-pleasing, guilt, and over-functioning, so they reclaim sovereignty and agency in every part of life — from business and leadership to love and self-expression.""",
            supplemental_link_label="Explore the Golden Thread Spiral™",
            supplemental_link_url="#golden-thread",
            icon="fa-solid fa-lightbulb",
            layout_variant="centered_stack",
            background_style="light_surface",
            show_section=True,
            order=10
        )
        
        # ==================== FREE RESOURCE SECTION ====================
        self.stdout.write('Creating Free Resource Section...')
        free_resource = FreeResourceSection.objects.create(
            headline="Start Your Realignment Today",
            subheadline="Discover where you are in your spiral and what comes next.",
            body_text="""The 5 A's Framework for Authentic Alignment and Success isn't just theory. It's a diagnostic tool that shows you exactly where you are right now and what to do next.

Inside, you'll find:
• The complete 5 A's framework clearly broken down
• A diagnostic assessment to see which stage you're in
• Journaling prompts to deepen your clarity
• Practical exercises to move you forward
• Real examples from women in your exact situation

This is the same framework I use with my coaching clients — and it's yours free.""",
            primary_button_label="Download Your Free Framework",
            primary_button_url="#framework",
            primary_button_variant="primary",
            image_url="https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=600&h=800&fit=crop&q=80",
            image_alt_text="5 A's Framework for Authentic Alignment and Success workbook cover",
            image_position="right",
            layout_variant="two_column_text_image",
            background_style="light_surface",
            show_section=True,
            emphasize_as_key_section=True,
            order=11
        )
        
        # ==================== FOOTER SECTION ====================
        self.stdout.write('Creating Footer Section...')
        footer = FooterSection.objects.create(
            brand_line="Insight Seeker: Impact by Design",
            tagline="Stop surviving. Start designing.",
            phone="760-205-3501",
            email="Connect@KimHerrlein.com",
            location_line="West Coast Base | Global Reach | Online Programs",
            legal_line="Privacy Policy | Accessibility Statement",
            copyright_text="Insight Seeker: Impact by Design",
            layout_variant="multi_column",
            background_style="dark_band",
            show_section=True,
            order=12
        )
        
        SocialLink.objects.create(
            section=footer,
            platform="instagram",
            label="Instagram",
            url="https://instagram.com/kimherrlein",
            icon="fab fa-instagram",
            order=0
        )
        SocialLink.objects.create(
            section=footer,
            platform="linkedin",
            label="LinkedIn",
            url="https://linkedin.com/in/kimherrlein",
            icon="fab fa-linkedin",
            order=1
        )
        SocialLink.objects.create(
            section=footer,
            platform="facebook",
            label="Facebook",
            url="https://facebook.com/kimherrlein",
            icon="fab fa-facebook",
            order=2
        )
        
        FooterLink.objects.create(
            section=footer,
            label="Privacy Policy",
            url="#privacy",
            order=0
        )
        FooterLink.objects.create(
            section=footer,
            label="Accessibility Statement",
            url="#accessibility",
            order=1
        )
        
        # ==================== CREATE PAGE WITH SECTIONS FOR DASHBOARD ====================
        self.stdout.write('Creating Page with Sections for Dashboard...')
        
        # Create or get Homepage
        homepage, created = Page.objects.get_or_create(
            slug='home',
            defaults={
                'name': 'Homepage',
                'description': 'Your main homepage - the first page visitors see',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write('Created Homepage for dashboard editing')
        else:
            # Clear existing sections if page already exists
            homepage.sections.all().delete()
            self.stdout.write('Cleared existing sections, recreating...')
        
        # Create Section for Hero
        Section.objects.create(
            page=homepage,
            section_type='hero',
            internal_label='Homepage Hero',
            sort_order=1,
            is_enabled=True,
            section_config={
                'headline': hero.headline,
                'subheadline': hero.subheadline,
                'body_text': hero.body_text,
                'quote_text': hero.quote_text,
                'quote_attribution': hero.quote_attribution,
                'primary_button': {
                    'label': hero.primary_button_label,
                    'url': hero.primary_button_url,
                    'variant': hero.primary_button_variant
                },
                'secondary_button': {
                    'label': hero.secondary_button_label,
                    'url': hero.secondary_button_url,
                    'variant': hero.secondary_button_variant
                },
                'image': {
                    'url': hero.image_url,
                    'alt_text': hero.image_alt_text
                },
                'icon': hero.icon,
                'layout_variant': hero.layout_variant,
                'background_style': hero.background_style,
                'show_section': hero.show_section,
                'show_divider_below': hero.show_divider_below,
            }
        )
        
        # Create Section for Statistics
        stats_config = {
            'headline': stats.headline,
            'intro_text': stats.intro_text,
            'stats': [
                {
                    'label': item.label,
                    'value': item.value,
                    'description': item.description,
                    'icon': item.icon
                } for item in stats.statitem_set.all()
            ],
            'primary_button': {
                'label': stats.primary_button_label,
                'url': stats.primary_button_url,
                'variant': stats.primary_button_variant
            },
            'layout_variant': stats.layout_variant,
            'background_style': stats.background_style,
        }
        Section.objects.create(
            page=homepage,
            section_type='statistics',
            internal_label='Statistics Section',
            sort_order=2,
            is_enabled=stats.show_section,
            section_config=stats_config
        )
        
        # Create Section for Credibility
        credibility_config = {
            'headline': credibility.headline,
            'subheadline': credibility.subheadline,
            'intro_text': credibility.intro_text,
            'credibility_items': [
                {
                    'title': item.title,
                    'body_text': item.body_text,
                    'icon': item.icon,
                    'highlight': item.highlight
                } for item in credibility.credibilityitem_set.all()
            ],
            'image': {
                'url': credibility.image_url,
                'alt_text': credibility.image_alt_text
            },
            'primary_button': {
                'label': credibility.primary_button_label,
                'url': credibility.primary_button_url,
                'variant': credibility.primary_button_variant
            },
            'layout_variant': credibility.layout_variant,
            'background_style': credibility.background_style,
        }
        Section.objects.create(
            page=homepage,
            section_type='credibility',
            internal_label='Credibility Section',
            sort_order=3,
            is_enabled=credibility.show_section,
            section_config=credibility_config
        )
        
        # Create Section for Testimonials
        testimonials_config = {
            'headline': testimonials.headline,
            'subheadline': testimonials.subheadline,
            'testimonials': [
                {
                    'quote': t.quote,
                    'name': t.name,
                    'role_or_context': t.role_or_context,
                    'image': {
                        'url': t.image_url,
                        'alt_text': t.image_alt_text
                    },
                    'highlight': t.highlight
                } for t in testimonials.testimonial_set.all()
            ],
            'primary_button': {
                'label': testimonials.primary_button_label,
                'url': testimonials.primary_button_url,
                'variant': testimonials.primary_button_variant
            },
            'layout_variant': testimonials.layout_variant,
            'background_style': testimonials.background_style,
        }
        Section.objects.create(
            page=homepage,
            section_type='testimonials',
            internal_label='Testimonials Section',
            sort_order=4,
            is_enabled=testimonials.show_section,
            section_config=testimonials_config
        )
        
        # Create Section for Pain Points
        pain_points_config = {
            'headline': pain_points.headline,
            'subheadline': pain_points.subheadline,
            'intro_text': pain_points.intro_text,
            'pain_points': [
                {
                    'pain_quote': pp.pain_quote,
                    'description': pp.description,
                    'what_changes_label': pp.what_changes_label,
                    'what_changes_body': pp.what_changes_body,
                    'icon_pain': pp.icon_pain,
                    'icon_solution': pp.icon_solution
                } for pp in pain_points.painpoint_set.all()
            ],
            'golden_thread_quote_text': pain_points.golden_thread_quote_text,
            'golden_thread_quote_attribution': pain_points.golden_thread_quote_attribution,
            'primary_button': {
                'label': pain_points.primary_button_label,
                'url': pain_points.primary_button_url,
                'variant': pain_points.primary_button_variant
            },
            'layout_variant': pain_points.layout_variant,
            'background_style': pain_points.background_style,
        }
        Section.objects.create(
            page=homepage,
            section_type='pain_points',
            internal_label='Pain Points & Solutions',
            sort_order=5,
            is_enabled=pain_points.show_section,
            section_config=pain_points_config
        )
        
        # Create Section for What Makes Me Different
        different_config = {
            'headline': different.headline,
            'subheadline': different.subheadline,
            'intro_text': different.intro_text,
            'differentiator_cards': [
                {
                    'title': card.title,
                    'body_text': card.body_text,
                    'example_text': card.example_text,
                    'icon': card.icon
                } for card in different.differentiatorcard_set.all()
            ],
            'primary_button': {
                'label': different.primary_button_label,
                'url': different.primary_button_url,
                'variant': different.primary_button_variant
            },
            'layout_variant': different.layout_variant,
            'background_style': different.background_style,
        }
        Section.objects.create(
            page=homepage,
            section_type='what_makes_me_different',
            internal_label='What Makes Me Different',
            sort_order=6,
            is_enabled=different.show_section,
            section_config=different_config
        )
        
        # Create Section for Featured Publications
        publications_config = {
            'headline': publications.headline,
            'subheadline': publications.subheadline,
            'intro_text': publications.intro_text,
            'publications': [
                {
                    'title': pub.title,
                    'subtitle': pub.subtitle,
                    'description': pub.description,
                    'button_label': pub.button_label,
                    'button_url': pub.button_url,
                    'image': {
                        'url': pub.image_url,
                        'alt_text': pub.image_alt_text
                    }
                } for pub in publications.publication_set.all()
            ],
            'layout_variant': publications.layout_variant,
            'background_style': publications.background_style,
        }
        Section.objects.create(
            page=homepage,
            section_type='featured_publications',
            internal_label='Featured Publications',
            sort_order=7,
            is_enabled=publications.show_section,
            section_config=publications_config
        )
        
        # Create Section for Services
        services_config = {
            'headline': services.headline,
            'subheadline': services.subheadline,
            'intro_quote': services.intro_quote,
            'intro_quote_attribution': services.intro_quote_attribution,
            'services': [
                {
                    'name': svc.name,
                    'short_label': svc.short_label,
                    'description': svc.description,
                    'bullets': svc.bullets,
                    'cohort_details': svc.cohort_details,
                    'pricing_note': svc.pricing_note,
                    'primary_button': {
                        'label': svc.primary_button_label,
                        'url': svc.primary_button_url,
                        'variant': svc.primary_button_variant
                    },
                    'image': {
                        'url': svc.image_url,
                        'alt_text': svc.image_alt_text
                    },
                    'icon': svc.icon
                } for svc in services.service_set.all()
            ],
            'layout_variant': services.layout_variant,
            'background_style': services.background_style,
        }
        Section.objects.create(
            page=homepage,
            section_type='services',
            internal_label='Services Section',
            sort_order=8,
            is_enabled=services.show_section,
            section_config=services_config
        )
        
        # Create Section for Meet Kim
        meet_kim_config = {
            'headline': meet_kim.headline,
            'subheadline': meet_kim.subheadline,
            'body_text': meet_kim.body_text,
            'quote_text': meet_kim.quote_text,
            'quote_attribution': meet_kim.quote_attribution,
            'image': {
                'url': meet_kim.image_url,
                'alt_text': meet_kim.image_alt_text
            },
            'primary_button': {
                'label': meet_kim.primary_button_label,
                'url': meet_kim.primary_button_url,
                'variant': meet_kim.primary_button_variant
            },
            'layout_variant': meet_kim.layout_variant,
            'background_style': meet_kim.background_style,
        }
        Section.objects.create(
            page=homepage,
            section_type='meet_kim',
            internal_label='Meet Kim Herrlein',
            sort_order=9,
            is_enabled=meet_kim.show_section,
            section_config=meet_kim_config
        )
        
        # Create Section for Mission
        mission_config = {
            'headline': mission.headline,
            'body_text': mission.body_text,
            'supplemental_link_label': mission.supplemental_link_label,
            'supplemental_link_url': mission.supplemental_link_url,
            'icon': mission.icon,
            'layout_variant': mission.layout_variant,
            'background_style': mission.background_style,
        }
        Section.objects.create(
            page=homepage,
            section_type='mission',
            internal_label='Mission Section',
            sort_order=10,
            is_enabled=mission.show_section,
            section_config=mission_config
        )
        
        # Create Section for Free Resource
        free_resource_config = {
            'headline': free_resource.headline,
            'subheadline': free_resource.subheadline,
            'body_text': free_resource.body_text,
            'primary_button': {
                'label': free_resource.primary_button_label,
                'url': free_resource.primary_button_url,
                'variant': free_resource.primary_button_variant
            },
            'image': {
                'url': free_resource.image_url,
                'alt_text': free_resource.image_alt_text
            },
            'image_position': free_resource.image_position,
            'layout_variant': free_resource.layout_variant,
            'background_style': free_resource.background_style,
        }
        Section.objects.create(
            page=homepage,
            section_type='free_resource',
            internal_label='Free Resource Section',
            sort_order=11,
            is_enabled=free_resource.show_section,
            section_config=free_resource_config
        )
        
        # Create Section for Footer
        footer_config = {
            'brand_line': footer.brand_line,
            'tagline': footer.tagline,
            'phone': footer.phone,
            'email': footer.email,
            'location_line': footer.location_line,
            'legal_line': footer.legal_line,
            'copyright_text': footer.copyright_text,
            'social_links': [
                {
                    'platform': sl.platform,
                    'label': sl.label,
                    'url': sl.url,
                    'icon': sl.icon
                } for sl in footer.sociallink_set.all()
            ],
            'footer_links': [
                {
                    'label': fl.label,
                    'url': fl.url
                } for fl in footer.footerlink_set.all()
            ],
            'layout_variant': footer.layout_variant,
            'background_style': footer.background_style,
        }
        Section.objects.create(
            page=homepage,
            section_type='footer',
            internal_label='Footer Section',
            sort_order=12,
            is_enabled=footer.show_section,
            section_config=footer_config
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded all content!'))
        self.stdout.write(self.style.SUCCESS(f'Created Homepage with {homepage.sections.count()} sections ready for dashboard editing!'))
        self.stdout.write('You can now view the website with all sections populated.')
        self.stdout.write('Go to /dashboard/ to edit your content.')

