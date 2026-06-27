#let resume(body) = {
  set list(indent: 0.5em)
  show list: set text(size: 0.90em)
  // show link: underline
  // show link: set underline(offset: 3pt, stroke: 0.5pt)

  set page(
    paper: "a4",
    margin: (x: 0.4in, y: 0.4in),
  )

  set text(
    size: 11pt,
    font: "Lato",
  )

  body
}

#let name_header(name) = {
  set text(size: 2.25em)
  [*#name*]
}

#let header(
  name: "Jake Ryan",
  phone: "123-456-7890",
  email: "jake@su.edu",
  linkedin: "linkedin.com/in/jake",
  github: "github.com/jake",
  portfolio: "jake.com",
) = {
  align(center, block[
    #name_header(name) \
    #link("mailto:" + email)[#email]  ┃
    #phone  ┃
    #link("https://" + portfolio)[#portfolio]  ┃
    #link("https://" + linkedin)[#linkedin]  ┃
    #link("https://" + github)[#github]
  ])
  v(5pt)
}

#let resume_heading(txt) = {
  show heading: set text(size: 0.92em, weight: "regular")

  block[
    = #smallcaps(txt)
    #v(-4pt)
    #line(length: 100%, stroke: 1pt + black)
  ]
}

#let edu_item(
  name: "Sample University",
  degree: "B.S in Bullshit",
  location: "Foo, BA",
  date: "Aug. 1600 - May 1750",
) = {
  set block(above: 0.7em, below: 1em)
  pad(left: 1em, right: 0.5em, grid(
    columns: (3fr, 1fr),
    align(left)[
      *#name* \
      _#degree _
    ],
    align(right)[
      #location \
      _#date _
    ],
  ))
}

#let exp_item(
  name: "Sample Workplace",
  role: "Worker",
  date: "June 1837 - May 1845",
  location: "Foo, BA",
  ..points,
) = {
  set block(above: 0.7em, below: 1em)
  pad(left: 1em, right: 0.5em, box[
    #grid(
      columns: (3fr, 1fr),
      align(left)[
        *#role* \
        _#name _
      ],
      align(right)[
        #date \
        _#location _
      ],
    )
    #v(-4pt)
    #list(..points.pos().map(p => eval(p, mode: "markup")))
  ])
}

#let project_item(
  name: "Example Project",
  skills: "Programming Language 1, Database3",
  date: "May 1234 - June 4321",
  url: "https://example.com",
  ..points,
) = {
  set block(above: 0.7em, below: 1em)
  pad(left: 1em, right: 0.5em, box[
    *#name* | _#skills _ | #link("https://" + url)[#url] #h(1fr) #date
    #list(..points.pos().map(p => eval(p, mode: "markup")))
  ])
}

#let skill_item(
  category: "Skills",
  skills: "Balling, Yoga, Valorant",
) = {
  set block(above: 0.7em)
  set text(size: 0.91em)
  pad(left: 1em, right: 0.5em, block[*#category*: #skills])
}
