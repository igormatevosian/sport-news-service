let skip = 0;
const limit = 5;

async function loadMoreArticles(articleTypeId) {
  let url = `/articles/?skip=${skip}&limit=${limit}`;
  if (articleTypeId) {
    url = `/articles/article_type/${articleTypeId}?skip=${skip}&limit=${limit}`;
  }

  const response = await fetch(url);
  const articles = await response.json();
  const container = document.getElementById("articles-container");

  for (const article of articles) {
    const articleElement = document.createElement("div");
    articleElement.classList.add("row", "align-items-center", "my-4");

    const ownerResponse = await fetch(`/users/${article.owner_id}`);
    const owner = await ownerResponse.json();

    articleElement.innerHTML = `
    <div class="col-md-12">
      <h2 class="featurette-heading"><a href="/article_detail/${article.id}">${
      article.title
    }</a></h2>
      <p class="lead">${article.short_description}</p>
      <p>Дата создания: ${new Date(
        article.created_date
      ).toLocaleDateString()}</p>
      <p>
          Автор:
            <a href="/user_page/${owner.id}">
            <img
        src="${owner.picture}"
        alt="${owner.name}"
        class="img-fluid rounded-circle"
        style="max-width: 3%"
      />${owner.name}
            </a>
        </p>
    </div>
  `;
    container.appendChild(articleElement);
  }

  skip += limit;
}
