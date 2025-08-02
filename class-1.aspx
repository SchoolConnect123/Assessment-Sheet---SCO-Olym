<%@ Page Language="C#" AutoEventWireup="true"
    CodeFile="class-1.aspx.cs"
    Inherits="olympiadbooks.Class1"
    MasterPageFile="~/scoMain.master" %>

<asp:Content ID="headContent" ContentPlaceHolderID="head" runat="server">
  <title>Class 1 Subjects | Olympiad Books</title>
<meta name="description" content="Explore all Olympiad subjects for Class 1 including AI, Math, Science, English, Coding, and more. Buy packages, register and prepare online.">
<meta name="keywords" content="Class 1 Olympiad, Math Olympiad, Science Olympiad, Coding Olympiad, Artificial Intelligence, School Connect Olympiad">
<meta name="robots" content="index, follow">
<meta property="og:title" content="Class 1 Olympiad Subjects | School Connect Online">
<meta property="og:description" content="Explore 14 Olympiad subjects for Class 1 students including Math, Science, AI, English and more.">
<meta property="og:image" content="https://www.schoolconnectonline.com/images/og/class-1.jpg">
<meta property="og:url" content="https://www.schoolconnectonline.com/olympiadbooks/class-1">
<meta name="twitter:card" content="summary_large_image">

<link rel="canonical" href="https://www.schoolconnectonline.com/olympiadbooks/class-1" />
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Class 1 Olympiad Subjects - School Connect",
  "url": "https://www.schoolconnectonline.com/olympiadbooks/class-1",
  "inLanguage": "en-IN"
}
</script>


  <style>
    /* ==== Page Container ==== */
    .page-block {
      background: #fff;
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      margin-bottom: 2rem;
      padding: 1.5rem;

.page-block {
  border-left: 5px solid #015DE9;
  box-shadow: 0 2px 12px rgba(1, 93, 233, 0.1);
}


.container {
  background: #fefefe;
  padding-top: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

    }
    /* ==== Heading ==== */
    .page-block h3 {
      margin-top: 0;
      color: #015DE9;
      font-size: 1.5rem;
      border-bottom: 2px solid #015DE9;
      padding-bottom: 0.5rem;
      margin-bottom: 1rem;
    }
    /* ==== Layout ==== */
    .two-col {
      display: flex;
      flex-wrap: wrap;
      gap: 1.5rem;
    }
    .main-col { flex: 1 1 60%; }
    .side-col { flex: 1 1 35%; }

    /* ==== Subject Grid ==== */
    .subject-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1rem;
    }

.subject-card {
  background: linear-gradient(135deg, #015DE9, #3F89FC);
  color: #fff;
  padding: 1rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: bold;
  transition: all 0.3s ease-in-out;
}
.subject-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 20px rgba(1, 93, 233, 0.3);
}


.subject-info {
  margin-top: 1rem;
}
.seo-block {
  background: #ffffff;
  padding: 1.25rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
  border-left-width: 5px;
  border-left-style: solid;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}


    /* ==== Sidebar Widgets ==== */
    .sidebar-widget {
      background: #f9f9f9;
      border: 1px solid #ddd;
      border-radius: 6px;
      padding: 1rem;
      margin-bottom: 1.5rem;
    }
    .sidebar-widget h4 {
      margin: 0 0 0.75rem;
      font-size: 1.25rem;
      color: #015DE9;
    }
     .btn-buy {
     display: block;
     width: 100%;
     margin-bottom: 1rem;
     background-color: #015DE9;
     color: #fff;
     padding: 0.6rem 1rem;
     border-radius: 4px;
     text-align: center;
     font-weight: bold;
     text-decoration: none;
     }
    .btn-buy:hover {
     background-color: #013cad;
     color: #fff;
    }
    .widget-ad {
      background: #e6f2ff;
      height: 200px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #666;
      font-style: italic;
      border: 1px dashed #b3d7ff;
      border-radius: 6px;
    }

    /* ==== Info Blocks ==== */
    .subject-info h2 {
      font-size: 1.25rem;
      color: #015DE9;
      margin-top: 1.5rem;
      margin-bottom: 0.5rem;
      border-bottom: 1px solid #ddd;
      padding-bottom: 0.3rem;
    }
    .subject-info p {
      margin-bottom: 1rem;
      line-height: 1.6;
    }

    /* ==== Responsive ==== */
    @media (max-width: 768px) {
      .two-col { flex-direction: column; }
    }
  </style>
</asp:Content>

<asp:Content ID="mainContent" ContentPlaceHolderID="mainContent" runat="server">
  <div class="container">

    <!-- Select Subject -->
    <div class="page-block">
      <h3>Select Your Subject (Class 1)</h3>
      <div class="subject-grid">
        <% 
          var subs = new[]
          {
            new { Slug="artificial-intelligence-olympiad", Name="Artificial Intelligence" },
            new { Slug="biology-olympiad",                Name="Biology" },
            new { Slug="chemistry-olympiad",              Name="Chemistry" },
            new { Slug="coding-olympiad",                 Name="Coding" },
            new { Slug="english-olympiad",                Name="English" },
            new { Slug="entrepreneurship-innovation-olympiad", Name="Entrepreneurship & Innovation" },
            new { Slug="finance-olympiad",                Name="Finance Olympiad" },
            new { Slug="general-knowledge-olympiad",      Name="General Knowledge" },
            new { Slug="life-skill-olympiad",             Name="LifeÂ Skill" },
            new { Slug="math-olympiad",                   Name="Mathematics" },
            new { Slug="mental-ability-olympiad",         Name="MentalÂ Ability" },
            new { Slug="physics-olympiad",                Name="Physics" },
            new { Slug="science-olympiad",                Name="Science" },
            new { Slug="social-studies-olympiad",         Name="Social Studies" }
          };
          for(int i=0;i<subs.Length;i++){
            var s=subs[i];
        %>
          <a href="/olympiadbooks/class-1/<%=s.Slug%>" class="subject-card">
            <%=s.Name%>
          </a>
        <% } %>
      </div>
    </div>

    <div class="two-col">
      <!-- Main Column -->
      <div class="main-col">

        <!-- Info Section -->


<!-- SEO Section - Inside main-col so sidebar stays aligned -->
<div class="subject-info">
  <div class="seo-block" style="border-left: 5px solid #FF6F61;">
    <h2>Artificial Intelligence Olympiad (Class 1)</h2>
    <p>Write SEO content for Artificial Intelligence here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #42A5F5;">
    <h2>Biology Olympiad (Class 1)</h2>
    <p>Write SEO content for Biology here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #66BB6A;">
    <h2>Chemistry Olympiad (Class 1)</h2>
    <p>Write SEO content for Chemistry here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #AB47BC;">
    <h2>Coding Olympiad (Class 1)</h2>
    <p>Write SEO content for Coding here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #FF7043;">
    <h2>English Olympiad (Class 1)</h2>
    <p>Write SEO content for English here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #29B6F6;">
    <h2>Entrepreneurship & Innovation Olympiad (Class 1)</h2>
    <p>Write SEO content for Entrepreneurship & Innovation here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #FFA726;">
    <h2>Finance Olympiad (Class 1)</h2>
    <p>Write SEO content for Finance here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #66BB6A;">
    <h2>General Knowledge Olympiad (Class 1)</h2>
    <p>Write SEO content for General Knowledge here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #BA68C8;">
    <h2>Life Skill Olympiad (Class 1)</h2>
    <p>Write SEO content for Life Skills here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #42A5F5;">
    <h2>Mathematics Olympiad (Class 1)</h2>
    <p>Write SEO content for Mathematics here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #FF8A65;">
    <h2>Mental Ability Olympiad (Class 1)</h2>
    <p>Write SEO content for Mental Ability here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #26C6DA;">
    <h2>Physics Olympiad (Class 1)</h2>
    <p>Write SEO content for Physics here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #EC407A;">
    <h2>Science Olympiad (Class 1)</h2>
    <p>Write SEO content for Science here.</p>
  </div>
  <div class="seo-block" style="border-left: 5px solid #7E57C2;">
    <h2>Social Studies Olympiad (Class 1)</h2>
    <p>Write SEO content for Social Studies here.</p>
  </div>
</div>


      </div>

      <!-- Sidebar -->
      <div class="side-col">
        <!-- Buy Widget -->
        <div class="sidebar-widget">
          <h4>Buy Full Class 1 Package</h4>
          <a href="/buy/class-1" class="btn-buy">
            <i class="fa fa-shopping-cart"></i> Buy Full Package
          </a>
          <h4>Related Links</h4>
          <ul>
            <% foreach(var s in subs) { %>
              <li><a href="/olympiadbooks/class-1/<%=s.Slug%>"><%=s.Name %> Olympiad</a></li>
            <% } %>
          </ul>
        </div>

        <!-- Ad Widget 1 -->
<div class="sidebar-widget widget-ad">
  <a href="https://www.schoolconnectonline.com/packages" target="_blank">
    <img src="/images/ads/ai-pack.jpg" alt="AI Olympiad Pack" style="width:100%; border-radius:6px;" />
  </a>
</div>

<!-- Ad Widget 2 -->
<div class="sidebar-widget widget-ad">
  <a href="https://www.schoolconnectonline.com/register" target="_blank">
    <img src="/images/ads/register-now.jpg" alt="Register for Olympiad" style="width:100%; border-radius:6px;" />
  </a>
</div>

<!-- Ad Widget 3 -->
<div class="sidebar-widget widget-ad">
  <a href="https://www.schoolconnectonline.com/free-sample-papers" target="_blank">
    <img src="/images/ads/sample-papers.jpg" alt="Free Sample Papers" style="width:100%; border-radius:6px;" />
  </a>
</div>

<!-- Ad Widget 4 -->
<div class="sidebar-widget widget-ad">
  <a href="https://www.schoolconnectonline.com/testimonials" target="_blank">
    <img src="/images/ads/student-reviews.jpg" alt="Student Testimonials" style="width:100%; border-radius:6px;" />
  </a>
</div>

<!-- Ad Widget 5 -->
<div class="sidebar-widget widget-ad">
  <a href="https://www.schoolconnectonline.com/results" target="_blank">
    <img src="/images/ads/topper-list.jpg" alt="Topper Results" style="width:100%; border-radius:6px;" />
  </a>
</div>

      </div>
    </div>
  </div>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Class 1 Olympiad Subjects",
  "description": "List of Class 1 Olympiad Subjects offered by School Connect Olympiad, including AI, Coding, Science, Math, English, and more.",
  "url": "https://www.schoolconnectonline.com/olympiadbooks/class-1",
  "numberOfItems": 14,
  "itemListElement": [
    <% for(int i=0; i<subs.Length; i++) { var s = subs[i]; %>
    {
      "@type": "ListItem",
      "position": <%= i+1 %>,
      "name": "<%= s.Name %> Olympiad",
      "url": "https://www.schoolconnectonline.com/olympiadbooks/class-1/<%= s.Slug %>"
    }<%= i < subs.Length-1 ? "," : "" %>
    <% } %>
  ]
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    <% for(int i=0; i<subs.Length; i++) {
         var s = subs[i];
         var name = s.Name + " Olympiad - Class 1";
         var url = "https://www.schoolconnectonline.com/olympiadbooks/class-1/" + s.Slug;
    %>
    {
      "@type": "Product",
      "name": "<%= name %>",
      "image": "https://www.schoolconnectonline.com/images/subjects/<%= s.Slug %>.jpg",
      "description": "Buy Mock Tests, Workbooks, Worksheets, Sample Papers for <%= name %>",
      "brand": {
        "@type": "Brand",
        "name": "School Connect Olympiad"
      },
      "offers": {
        "@type": "Offer",
        "url": "<%= url %>",
        "priceCurrency": "INR",
        "price": "199",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition"
      }
    }<%= i < subs.Length - 1 ? "," : "" %>
    <% } %>
  ]
}
</script>


</asp:Content>

<asp:Content ID="endScripts" ContentPlaceHolderID="endScripts" runat="server">
  <!-- no extra scripts needed -->
</asp:Content>

