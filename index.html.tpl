<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="When will the next leap second happen?">
    <title>Leap Second Prediction</title>

    <link rel="canonical" href="https://565851109.xyz/">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⏰</text></svg>">

    <!-- Bootstrap core CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
    <meta name="theme-color" content="#7952b3">

    <!--
      -- Data is also available in JSON format
      -- Schema is likely to change in the future!
      -->
    <link href="index.json" rel="alternate" type="application/json">

    <script async src="https://www.googletagmanager.com/gtag/js?id=G-KBT3MY235W"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-KBT3MY235W');
    </script>

    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
    </style>
  </head>
  <body>
    <main>
      <div class="container py-4">
        <header class="pb-3 mb-4 border-bottom">

          <a href="/" class="d-flex align-items-center text-dark text-decoration-none">
            <span class="fs-4">When will the next leap second happen?</span>
          </a>
        </header>

        <div class="p-5 mb-4 bg-light rounded-3">
          <div class="container-fluid py-5">
            <p class="col-md-8 fs-6">Based on <a href="{{ source.url }}">IERS Bulletin A Vol. {{ source.issue }} No. {{ source.number }}</a>, and making some very large, probably unjustified assumptions;</p>
            {% if next_leap_second %}
            <p class="col-md-8 fs-4">at <a>the end of {% if next_leap_second.month == 7 %}June, {{ next_leap_second.year }}{% else %}December, {{ next_leap_second.year - 1 }}{% endif %}</b></p>
            {% if next_leap_second.is_positive %}
            <p class="col-md-8 fs-5">And will be a positive leap second</p>
            {% else %}
            <p class="col-md-8 fs-5">And will be a negative leap second</p>
            {% endif %}
            {% else %}
            <p class="col-md-8 fs-4">no leap second is predicted for the next 50 years</p>
            {% endif %}
          </div>
        </div>

        <div class="row align-items-md-stretch">
          <div class="col-md-6">
            <div class="h-100 p-5 bg-light border rounded-3">
              <h2>How did you calculate that?</h2>
              <p class="fs-6">
                Based on <a href="https://github.com/fanf2/bulletin-a">some great work</a> by <a href="https://twitter.com/fanf/">Tony Finch</a>, I'm parsing the text of the IERS Bulletin A notice to find the parameters provided to predict the difference between UT1 (solar time) and UTC (civil time). Once I have those values, I calculate the predicted difference going forward for the start of July and January each year until the absolute difference is more than 0.5 seconds. The Bulletin A parameters really aren't intended to be used to make predictions that far in the future, and are based on a model that assumes that the change in UT1-UTC is more or less linear, which <a href="https://datacenter.iers.org/singlePlot.php?plotname=BulletinA_All-UT1-UTC&id=6">hasn't been the case</a> recently.
              </p>
              <p class="fs-8">tl;dr: Magic and guesswork. Take all of this with a giant pinch of salt. Source code is available <a href="https://github.com/insertjokehere/leap-second-prediction/">on GitHub</a>.</p>
              <p class="fs-8">This page updates automatically once a week when the new bulletin is published.</p>
            </div>
          </div>
          <div class="col-md-6">
            <div class="h-100 p-5 bg-light border rounded-3">
              <h2>What does that mean?</h2>
              <p>All the clocks you encounter in your day-to-day life set their time according to a system called UTC which assumes that the length of a year doesn't change over time. Unfortunately, reality isn't that tidy, and the rotation of the earth has actually been slowing down for (at least) the last few decades. In order to keep the "civil" time that most people use from getting too far out of sync with "solar" time, the people in charge of UTC add an extra second to the last minute of June or December if they determine that things are getting too far out of sync.</p>
              <p>Interestingly, Earths' rotation stopped slowing down towards the end of 2019, and in 2020 the trend reversed and the planets rotation started speeding up again. It's not entirely clear what caused this, but an interesting side effect might be the need to <i>remove</i> a second from UTC. This is called a "negative" leap second, and has never been done before.</p>
            </div>
          </div>
        </div>

        <footer class="pt-3 mt-4 text-muted border-top">
          Last updated {{ last_updated }}Z
        </footer>
      </div>
    </main>
  </body>
</html>
