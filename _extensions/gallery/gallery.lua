-- {{< gallery >}}: renders the page's `gallery:` front matter
-- (list of {src, caption}) as a Bootstrap carousel with lightbox links.
-- A single item renders as a plain figure; .mp4 sources render as video.

local counter = 0

local function esc(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

local function media(src, caption, gallery_id)
  if src:match("%.mp4$") then
    return '<video class="d-block w-100" autoplay loop muted playsinline aria-label="' .. caption ..
      '"><source src="' .. src .. '" type="video/mp4"></video>'
  end
  return '<a href="' .. src .. '" class="lightbox" data-gallery="' .. gallery_id ..
    '" data-description="' .. caption .. '"><img src="' .. src ..
    '" class="d-block w-100" alt="' .. caption .. '"></a>'
end

return {
  ["gallery"] = function(args, kwargs, meta)
    local items = meta.gallery
    if items == nil or #items == 0 then
      return pandoc.Null()
    end

    counter = counter + 1
    local id = "gallery-" .. counter

    if #items == 1 then
      local src = pandoc.utils.stringify(items[1].src)
      local caption = esc(pandoc.utils.stringify(items[1].caption or ""))
      return pandoc.RawBlock("html",
        '<figure class="research-figure">' .. media(src, caption, id) ..
        '<figcaption>' .. caption .. '</figcaption></figure>')
    end

    local slides = {}
    for i, item in ipairs(items) do
      local src = pandoc.utils.stringify(item.src)
      local caption = esc(pandoc.utils.stringify(item.caption or ""))
      table.insert(slides,
        '<div class="carousel-item' .. (i == 1 and ' active' or '') .. '">' ..
        media(src, caption, id) ..
        '<div class="carousel-caption"><p>' .. caption .. '</p></div></div>')
    end

    return pandoc.RawBlock("html",
      '<div id="' .. id .. '" class="carousel slide" data-bs-ride="carousel">' ..
      '<div class="carousel-inner">' .. table.concat(slides) .. '</div>' ..
      '<button class="carousel-control-prev" type="button" data-bs-target="#' .. id ..
      '" data-bs-slide="prev" aria-label="Previous"><span class="carousel-control-prev-icon"></span></button>' ..
      '<button class="carousel-control-next" type="button" data-bs-target="#' .. id ..
      '" data-bs-slide="next" aria-label="Next"><span class="carousel-control-next-icon"></span></button>' ..
      '</div>')
  end
}
